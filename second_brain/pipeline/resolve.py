"""Entity resolution — Phase A: deterministic, high-precision matchers.

The slug-identity baseline (`slugify(label)`) already has B-Cubed precision
1.000; the whole gap to the 0.85 target is recall. So Phase A adds only
*deterministic, high-precision* matchers that recover obvious coreference the
slug rule misses, without dragging precision down:

  - normalized-equal : case / punctuation / underscore variants
                       ("pit_bull" ↔ "Pit Bull", "U.S. FDA" ↔ "us fda")
  - plural           : singular ↔ plural ("...Terrier" ↔ "...Terriers")
  - acronym          : acronym ↔ expansion via exact stopword-skipping initials
                       ("AKC" ↔ "American Kennel Club", "ACVIM" ↔ "American
                       College of Veterinary Internal Medicine")
  - surname          : single token ↔ a person's full name
                       ("schenkel" ↔ "Rudolf Schenkel")

Deferred (later phases, see PLAN):
  - containment + embedding/string similarity ("Hill's" ↔ "Hill's Pet Nutrition")
  - LLM adjudication of pure synonyms ("Alsatian" ↔ "German Shepherd",
    "bloat" ↔ "GDV")

This stage is pure and side-effect-free: it produces a ResolutionResult
(clustering). Applying merges to the live LadybugDB graph is a separate,
destructive step (Phase D) that must go through the `ladybug-surgery` skill —
NOT done here.
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

# Words skipped when computing acronym initials and when deciding token overlap.
STOPWORDS = frozenset({
    "of", "the", "and", "for", "a", "an", "to", "in", "on", "&", "de", "von", "der",
})
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
    if len(word) > 4 and word.endswith("ies"):
        return word[:-3] + "y"
    if len(word) > 3 and word.endswith("es") and word[-3] in "sxzo":
        return word[:-2]
    if len(word) > 3 and word.endswith("s") and not word.endswith("ss"):
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


MATCHERS = (match_normalized, match_plural, match_acronym, match_surname)


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

    def __init__(self, entities: list[dict]):
        # de-dup identical labels, keep first type seen
        self.types: dict[str, str] = {}
        for e in entities:
            label = (e.get("label") or "").strip()
            if label and label not in self.types:
                self.types[label] = (e.get("entity_type") or "").strip().lower()
        self.labels = list(self.types)

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
                    matches.append(ResolutionMatch(
                        left=a, right=b, rule=rule, confidence=conf, evidence=evidence))
                    break

        clusters = [
            ResolutionCluster(canonical=self._pick_canonical(group), members=sorted(group))
            for group in uf.groups()
        ]
        # stable order: largest clusters first, then by canonical
        clusters.sort(key=lambda c: (-len(c.members), c.canonical.lower()))
        return ResolutionResult(clusters=clusters, matches=matches)

    @staticmethod
    def _pick_canonical(group: list[str]) -> str:
        """Prefer the most descriptive surface form: most tokens, then longest,
        then a form containing an uppercase letter (a proper name over a slug)."""
        return max(
            group,
            key=lambda l: (len(tokens(l)), len(l), any(c.isupper() for c in l)),
        )
