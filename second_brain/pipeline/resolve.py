"""Entity resolution.

The slug-identity baseline (`slugify(label)`) has B-Cubed precision 1.000 on
`eval/er_gold.json` but recall 0.510 (F1 0.675); the whole gap to the 0.85
target is recall. The resolver recovers coreference the slug rule misses while
holding precision.

Phase A — deterministic, high-precision matchers:
  - normalized-equal : case / punctuation / underscore variants
  - plural           : singular ↔ plural ("...Terrier" ↔ "...Terriers")
  - acronym          : acronym ↔ expansion via exact stopword-skipping initials
                       ("AKC" ↔ "American Kennel Club"), with a proper-name guard
                       so "CDC" does NOT match "canine dilated cardiomyopathy"
  - surname          : single token ↔ a person's full name (person-typed)

Phase B — looser/similarity matchers:
  - acronym-subseq   : acronym ⊆ initials ("FDA" ⊆ "U.S. Food and Drug Admin.")
  - legal-suffix     : "X" ↔ "X Inc." (corporate-suffix-only difference)
  - embedding        : cosine ≥ DEDUP_THRESHOLD (0.92) AND compatible type.
                       Own kNN blocking (synonyms share no token). On the graph's
                       real vectors this lifts F1 to 0.874; the 0.92 cliff is
                       sharp (0.90 collapses precision), so the threshold is a
                       guard, not a tuning knob.

Deferred:
  - Phase C: LLM adjudication of pure synonyms with no shared string/cheap-vector
    signal ("Alsatian" ↔ "German Shepherd", "bloat" ↔ "GDV").
  - Phase D: APPLYING merges to the live LadybugDB graph (repoint edges, fold
    aliases, delete dup nodes) — destructive; must go through the
    `ladybug-surgery` skill. This module only PROPOSES (pure ResolutionResult).
"""

from __future__ import annotations

import re
import unicodedata
from collections import defaultdict

from second_brain.models.resolution import (
    ResolutionCluster,
    ResolutionMatch,
    ResolutionResult,
)
from second_brain.ontology import slugify

# Words skipped when computing acronym initials and when deciding token overlap.
STOPWORDS = frozenset(
    {
        "of",
        "the",
        "and",
        "for",
        "a",
        "an",
        "to",
        "in",
        "on",
        "&",
        "de",
        "von",
        "der",
    }
)
# Leading honorifics stripped before surname matching.
HONORIFICS = frozenset({"dr", "mr", "mrs", "ms", "prof", "professor", "sir", "dame"})


def normalize(label: str) -> str:
    """Lowercase, strip accents/punctuation, collapse whitespace.

    "U.S. FDA" -> "us fda";  "Hill's Pet Nutrition" -> "hills pet nutrition";
    "dominance_theory" -> "dominance theory";  "Fédération" -> "federation".
    """
    if not label:
        return ""
    # strip accents
    decomposed = unicodedata.normalize("NFKD", label)
    ascii_ish = "".join(c for c in decomposed if not unicodedata.combining(c))
    lowered = ascii_ish.lower()
    # non-alphanumeric -> space (apostrophes vanish so "hill's" -> "hills")
    spaced = re.sub(r"[^a-z0-9]+", " ", lowered.replace("'", ""))
    return " ".join(spaced.split())


def tokens(label: str) -> list[str]:
    return normalize(label).split()


def _singularize(word: str) -> str:
    # Words that look plural but aren't: "basis", "canis", "status", "class".
    if word.endswith(("is", "us", "ss", "ous")):
        return word
    if len(word) > 4 and word.endswith("ies"):
        return word[:-3] + "y"
    if len(word) > 3 and word.endswith("es") and word[-3] in "sxzo":
        return word[:-2]
    if len(word) > 3 and word.endswith("s"):
        return word[:-1]
    return word


def singular_key(label: str) -> str:
    """Normalized form with the LAST token singularized.

    "American Pit Bull Terriers" -> "american pit bull terrier";
    "pit bulls" -> "pit bull".
    """
    toks = tokens(label)
    if not toks:
        return ""
    return " ".join(toks[:-1] + [_singularize(toks[-1])])


def initials(label: str) -> str:
    """Stopword-skipping initials: "American College of Veterinary Internal
    Medicine" -> "acvim"."""
    return "".join(t[0] for t in tokens(label) if t and t not in STOPWORDS)


def is_acronym_form(label: str) -> bool:
    """A single alphabetic token of length 2-6 — candidate to be an acronym."""
    toks = tokens(label)
    return len(toks) == 1 and 2 <= len(toks[0]) <= 6 and toks[0].isalpha()


def _strip_honorifics(toks: list[str]) -> list[str]:
    i = 0
    while i < len(toks) and toks[i] in HONORIFICS:
        i += 1
    return toks[i:]


# --------------------------------------------------------------------------- #
# Pairwise matchers. Each takes (label_a, type_a, label_b, type_b) and returns
# (rule, confidence, evidence) if it fires, else None. Conventions:
#   - never match a label to itself
#   - high precision over recall (Phase A)
# --------------------------------------------------------------------------- #


def match_normalized(la, ta, lb, tb):
    if la == lb:
        return None
    if normalize(la) == normalize(lb) and normalize(la):
        return ("normalized-equal", 0.95, f"normalize → {normalize(la)!r}")
    return None


def match_plural(la, ta, lb, tb):
    if normalize(la) == normalize(lb):
        return None  # already caught by normalized-equal
    ka, kb = singular_key(la), singular_key(lb)
    if ka and ka == kb:
        return ("plural", 0.9, f"singular key → {ka!r}")
    return None


def match_acronym(la, ta, lb, tb):
    a_acr, b_acr = is_acronym_form(la), is_acronym_form(lb)
    # exactly one side looks like an acronym, the other is multi-word
    if a_acr and not b_acr and len(tokens(lb)) >= 2:
        short, long_ = la, lb
    elif b_acr and not a_acr and len(tokens(la)) >= 2:
        short, long_ = lb, la
    else:
        return None
    # Precision guard: a real acronym expands to a PROPER NAME (capitalized
    # words) — "American Kennel Club" -> AKC. Block all-lowercase common-noun
    # phrases whose initials collide by coincidence: "canine dilated
    # cardiomyopathy" initials to "cdc", which must NOT merge with the org CDC.
    if not any(w[:1].isupper() for w in long_.split()):
        return None
    if normalize(short).replace(" ", "") == initials(long_):
        return ("acronym", 0.9, f"{normalize(short)} = initials({normalize(long_)})")
    return None


# Corporate/legal suffixes that don't change a company's identity.
LEGAL_SUFFIX = frozenset(
    {
        "inc",
        "incorporated",
        "llc",
        "ltd",
        "limited",
        "corp",
        "corporation",
        "co",
        "company",
        "gmbh",
        "plc",
    }
)


def _is_subsequence(short: str, long_: str) -> bool:
    it = iter(long_)
    return all(c in it for c in short)


def match_acronym_subsequence(la, ta, lb, tb):
    """Looser acronym match: the acronym is a *subsequence* (not exact prefix) of
    the expansion's initials — handles dropped country/function words, e.g.
    "FDA" <- "U.S. Food and Drug Administration" (initials "usfda")."""
    a_acr, b_acr = is_acronym_form(la), is_acronym_form(lb)
    if a_acr and not b_acr and len(tokens(lb)) >= 2:
        short, long_ = la, lb
    elif b_acr and not a_acr and len(tokens(la)) >= 2:
        short, long_ = lb, la
    else:
        return None
    if not any(w[:1].isupper() for w in long_.split()):  # proper-name guard
        return None
    s = normalize(short).replace(" ", "")
    ini = initials(long_)
    if len(s) < 3:  # 2-letter acronyms are too collision-prone for subsequence
        return None
    if s != ini and _is_subsequence(s, ini) and len(ini) <= len(s) + 3:
        return ("acronym-subseq", 0.8, f"{s} ⊆ initials({normalize(long_)})={ini}")
    return None


def match_legal_suffix(la, ta, lb, tb):
    """Merge "Hill's Pet Nutrition" ↔ "Hill's Pet Nutrition Inc." — identical
    token sets except for corporate-suffix tokens. Narrow on purpose: it will
    NOT merge "Hill's" ↔ "Hill's Pet Nutrition" (real words differ)."""
    a_set, b_set = set(tokens(la)), set(tokens(lb))
    if a_set == b_set or not a_set or not b_set:
        return None
    smaller, larger = (a_set, b_set) if len(a_set) < len(b_set) else (b_set, a_set)
    if smaller < larger and (larger - smaller) <= LEGAL_SUFFIX:
        return ("legal-suffix", 0.85, "differ only by a corporate suffix")
    return None


def match_surname(la, ta, lb, tb):
    # the multi-token side must be a person; single-token side is the surname
    def _try(single_label, single_type, full_label, full_type):
        if full_type != "person":
            return None
        s_toks = tokens(single_label)
        if len(s_toks) != 1 or len(s_toks[0]) < 3:
            return None
        f_toks = _strip_honorifics(tokens(full_label))
        if len(f_toks) >= 2 and f_toks[-1] == s_toks[0]:
            return ("surname", 0.85, f"{s_toks[0]!r} = surname of {normalize(full_label)!r}")
        return None

    return _try(la, ta, lb, tb) or _try(lb, tb, la, ta)


MATCHERS = (
    match_normalized,
    match_plural,
    match_acronym,
    match_acronym_subsequence,
    match_legal_suffix,
    match_surname,
)


def _cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(y * y for y in b) ** 0.5
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def _type_compatible(ta: str, tb: str) -> bool:
    """Embedding merges are allowed only within a type, or against the generic
    `concept`/unknown fallback — never between two distinct specific types."""
    if ta == tb:
        return True
    return "concept" in (ta, tb) or "" in (ta, tb)


class _UnionFind:
    def __init__(self, items):
        self.parent = {x: x for x in items}

    def find(self, x):
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[rb] = ra

    def groups(self):
        out = defaultdict(list)
        for x in self.parent:
            out[self.find(x)].append(x)
        return list(out.values())


class EntityResolver:
    """Deterministic Phase-A entity resolver.

    `entities` is a list of dicts with at least `label` and `entity_type`
    (extra keys ignored). Labels are the resolution items (matching the eval /
    gold convention). Resolution is pure — no graph writes.
    """

    def __init__(
        self,
        entities: list[dict],
        embeddings: dict[str, list[float]] | None = None,
        embedding_threshold: float | None = None,
    ):
        # de-dup identical labels, keep first type seen
        self.types: dict[str, str] = {}
        for e in entities:
            label = (e.get("label") or "").strip()
            if label and label not in self.types:
                self.types[label] = (e.get("entity_type") or "").strip().lower()
        self.labels = list(self.types)
        # Optional Tier-2 embedding similarity. Threshold defaults to
        # config.DEDUP_THRESHOLD (finally consumed). Vectors keyed by label.
        self.embeddings = {k: v for k, v in (embeddings or {}).items() if k in self.types}
        if embedding_threshold is None:
            try:
                from second_brain import config

                embedding_threshold = getattr(config, "DEDUP_THRESHOLD", 0.92)
            except Exception:
                embedding_threshold = 0.92
        self.embedding_threshold = embedding_threshold

    def _candidate_pairs(self) -> set[frozenset]:
        """Blocking: only pairs that share a non-stopword token, or an
        acronym↔initials bucket, are ever compared."""
        pairs: set[frozenset] = set()

        token_index: dict[str, list[str]] = defaultdict(list)
        initials_index: dict[str, list[str]] = defaultdict(list)
        acronyms: list[str] = []
        for label in self.labels:
            toks = [t for t in tokens(label) if t not in STOPWORDS]
            for t in set(toks):
                token_index[t].append(label)
            if len(toks) >= 2:
                initials_index[initials(label)].append(label)
            if is_acronym_form(label):
                acronyms.append(label)

        for members in token_index.values():
            for i in range(len(members)):
                for j in range(i + 1, len(members)):
                    pairs.add(frozenset((members[i], members[j])))

        for acr in acronyms:
            for long_ in initials_index.get(normalize(acr).replace(" ", ""), []):
                if long_ != acr:
                    pairs.add(frozenset((acr, long_)))

        return pairs

    def resolve(self) -> ResolutionResult:
        uf = _UnionFind(self.labels)
        matches: list[ResolutionMatch] = []

        for pair in self._candidate_pairs():
            a, b = tuple(pair) if len(pair) == 2 else (next(iter(pair)), next(iter(pair)))
            if a == b:
                continue
            for matcher in MATCHERS:
                res = matcher(a, self.types[a], b, self.types[b])
                if res:
                    rule, conf, evidence = res
                    uf.union(a, b)
                    matches.append(
                        ResolutionMatch(
                            left=a, right=b, rule=rule, confidence=conf, evidence=evidence
                        )
                    )
                    break

        # Tier 2 — embedding similarity (own blocking: kNN over vectors, since
        # synonyms like "Alsatian"/"German Shepherd" share no token). Type-guarded.
        matches.extend(self._embedding_matches(uf))

        clusters = [
            ResolutionCluster(canonical=self._pick_canonical(group), members=sorted(group))
            for group in uf.groups()
        ]
        # stable order: largest clusters first, then by canonical
        clusters.sort(key=lambda c: (-len(c.members), c.canonical.lower()))
        return ResolutionResult(clusters=clusters, matches=matches)

    def _embedding_matches(self, uf: "_UnionFind") -> list[ResolutionMatch]:
        """Union entity pairs whose embeddings are within threshold AND whose
        types are compatible. O(n^2) over embedded entities (fine at this scale)."""
        if len(self.embeddings) < 2:
            return []
        labels = list(self.embeddings)
        out: list[ResolutionMatch] = []
        for i in range(len(labels)):
            for j in range(i + 1, len(labels)):
                a, b = labels[i], labels[j]
                if not _type_compatible(self.types[a], self.types[b]):
                    continue
                sim = _cosine(self.embeddings[a], self.embeddings[b])
                if sim >= self.embedding_threshold:
                    uf.union(a, b)
                    out.append(
                        ResolutionMatch(
                            left=a,
                            right=b,
                            rule="embedding",
                            confidence=round(sim, 3),
                            evidence=f"cosine {sim:.3f} >= {self.embedding_threshold}",
                        )
                    )
        return out

    @staticmethod
    def _pick_canonical(group: list[str]) -> str:
        """Prefer the most descriptive surface form: most tokens, then longest,
        then a form containing an uppercase letter (a proper name over a slug)."""
        return max(
            group,
            key=lambda lbl: (len(tokens(lbl)), len(lbl), any(c.isupper() for c in lbl)),
        )


def canonicalize_extracted_graph(
    entities: list[dict],
    edges: list[dict],
) -> tuple[list[dict], list[dict], ResolutionResult]:
    """Resolve extracted entities before graph write and rewrite edge endpoints.

    This is intentionally non-destructive: it only rewrites the in-memory batch
    produced by extraction. Existing LadybugDB nodes/edges are not touched.
    """
    if not entities:
        return [], edges, EntityResolver([]).resolve()

    result = EntityResolver(entities).resolve()
    label_to_canonical = {
        member: cluster.canonical for cluster in result.clusters for member in cluster.members
    }
    label_to_canonical_id = {
        label: slugify(canonical) for label, canonical in label_to_canonical.items()
    }

    id_to_canonical_id: dict[str, str] = {}
    grouped: dict[str, list[dict]] = {}
    for entity in entities:
        label = (entity.get("label") or "").strip()
        if not label:
            continue
        canonical_id = label_to_canonical_id.get(label, slugify(label))
        if entity.get("id"):
            id_to_canonical_id[str(entity["id"])] = canonical_id
        grouped.setdefault(canonical_id, []).append(entity)

    canonical_entities = [_merge_entity_group(canonical_id, group) for canonical_id, group in grouped.items()]

    canonical_edges = []
    seen_edges = set()
    for edge in edges:
        source_id = id_to_canonical_id.get(str(edge.get("source_id", "")), edge.get("source_id"))
        target_id = id_to_canonical_id.get(str(edge.get("target_id", "")), edge.get("target_id"))
        if not source_id or not target_id or source_id == target_id:
            continue
        rewritten = {**edge, "source_id": source_id, "target_id": target_id}
        key = (
            rewritten.get("source_id"),
            rewritten.get("target_id"),
            rewritten.get("edge_type"),
            rewritten.get("evidence", ""),
        )
        if key in seen_edges:
            continue
        seen_edges.add(key)
        canonical_edges.append(rewritten)

    incident_ids = {
        edge_id
        for edge in canonical_edges
        for edge_id in (edge.get("source_id"), edge.get("target_id"))
        if edge_id
    }
    canonical_entities = [
        entity
        for entity in canonical_entities
        if entity.get("id") in incident_ids or not _is_unlinked_junk_entity(entity)
    ]

    return canonical_entities, canonical_edges, result


def _merge_entity_group(canonical_id: str, entities: list[dict]) -> dict:
    def confidence(entity: dict) -> float:
        try:
            return float(entity.get("confidence", 0.5))
        except (TypeError, ValueError):
            return 0.5

    canonical_label = EntityResolver._pick_canonical(
        [(e.get("label") or "").strip() for e in entities if (e.get("label") or "").strip()]
    )
    typed = [e for e in entities if (e.get("entity_type") or "concept") != "concept"]
    type_source = max(typed or entities, key=confidence)
    description_source = max(entities, key=lambda e: len(e.get("description") or ""))
    non_tag = [e for e in entities if e.get("provenance") != "obsidian_tag"]
    best = max(non_tag or entities, key=confidence)
    aliases = sorted({(e.get("label") or "").strip() for e in entities if e.get("label")})
    doc_ids = sorted(
        {
            doc_id
            for entity in entities
            for doc_id in ([entity.get("doc_id")] + list(entity.get("doc_ids") or []))
            if doc_id
        }
    )

    return {
        **best,
        "id": canonical_id,
        "entity_type": type_source.get("entity_type") or "concept",
        "label": canonical_label,
        "description": description_source.get("description", ""),
        "confidence": max(confidence(e) for e in entities),
        "aliases": aliases,
        "doc_id": doc_ids[0] if doc_ids else best.get("doc_id", ""),
        "doc_ids": doc_ids,
    }


def _is_unlinked_junk_entity(entity: dict) -> bool:
    """High-precision orphan filter for entities with no surviving edge.

    The graph should not persist navigation tags, bare years, URLs/file paths,
    or model-emitted slug literals as standalone semantic nodes. If any of these
    entities participates in an edge, keep it and let topology/evals judge it.
    """
    label = (entity.get("label") or "").strip()
    entity_id = str(entity.get("id") or "")
    entity_type = (entity.get("entity_type") or "").strip().lower()
    provenance = entity.get("provenance") or ""
    lower = label.lower()

    if provenance == "obsidian_tag" or entity_id.startswith("tag_"):
        return True
    if entity_type == "event" and len(label) == 4 and label.isdigit():
        year = int(label)
        if 1800 <= year <= 2099:
            return True
    if any(token in lower for token in ("http://", "https://", "www.", ".com", ".org")):
        return True
    if any(token in lower for token in (".md", ".pdf", "vault/", "ontology.yaml")):
        return True
    if _looks_like_generated_slug_literal(label):
        return True
    return False


def _looks_like_generated_slug_literal(label: str) -> bool:
    if not label or "_" not in label or " " in label or label.lower() != label:
        return False
    prefixes = (
        "concept_",
        "event_",
        "publication_",
        "location_",
        "product_",
        "organization_",
        "person_",
        "breed_",
    )
    return label.startswith(prefixes)
