#!/usr/bin/env python3
"""Visualize the knowledge graph with topological (homology) overlay.

Renders the entity-entity graph as an interactive HTML page:

  - Nodes colored by community (Louvain), sized by degree, hover shows
    label + entity type.
  - The H0/H1 persistent-homology reading (connected components and loops)
    is computed with Ripser and summarized on the page — H0 = how many
    disconnected islands, H1 = how many independent cycles (a cycle means
    several routes connect the same ideas, i.e. real structure rather than
    a tree).

Uses LadybugDB's native `get_as_networkx()` to pull the graph, NetworkX for
community + topology, Ripser for persistent homology, pyvis for the render.

Usage:
    python scripts/visualize.py                       # default graph + output
    python scripts/visualize.py --graph data/graph.lbug --out graph.html
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import ladybug as lb
except ImportError:
    import real_ladybug as lb

import networkx as nx


def load_graph_native(graph_path: str) -> nx.Graph:
    """Pull the entity-entity graph via LadybugDB's native get_as_networkx().

    Falls back to manual construction if the native export isn't available
    on this build.
    """
    db = lb.Database(graph_path, read_only=True, buffer_pool_size=256 * 1024 * 1024)
    conn = lb.Connection(db)
    res = conn.execute("MATCH (a:Entity)-[r]->(b:Entity) " "RETURN a, r, b")
    G: nx.Graph
    try:
        # Native export — directed multigraph; collapse to simple undirected
        # for topology (homology cares about connectivity, not direction).
        MG = res.get_as_networkx(directed=False)
        G = nx.Graph(MG)
    except Exception:
        # Fallback: manual build from a flat row query.
        G = nx.Graph()
        res2 = conn.execute(
            "MATCH (a:Entity)-[r]->(b:Entity) "
            "RETURN a.id AS src, a.label AS src_label, a.entity_type AS src_type, "
            "b.id AS tgt, b.label AS tgt_label, b.entity_type AS tgt_type, "
            "r.edge_type AS etype"
        )
        while res2.has_next():
            row = res2.get_next()
            src, src_label, src_type, tgt, tgt_label, tgt_type, etype = row
            G.add_node(src, label=src_label or src, entity_type=src_type or "concept")
            G.add_node(tgt, label=tgt_label or tgt, entity_type=tgt_type or "concept")
            G.add_edge(src, tgt, edge_type=etype or "RELATED")
    del conn, db
    return G


def homology(G: nx.Graph) -> dict:
    """Persistent homology via the project's topology helper."""
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from second_brain.topology import run_persistent_homology

    return run_persistent_homology(G)


def render(G: nx.Graph, homology_summary: dict, out_path: str) -> None:
    from pyvis.network import Network

    # Louvain communities for coloring
    try:
        from networkx.algorithms.community import louvain_communities

        comms = louvain_communities(G, seed=42) if len(G) else []
    except Exception:
        comms = list(nx.connected_components(G))
    node_comm = {}
    for i, c in enumerate(comms):
        for n in c:
            node_comm[n] = i

    palette = [
        "#e6194b",
        "#3cb44b",
        "#4363d8",
        "#f58231",
        "#911eb4",
        "#46f0f0",
        "#f032e6",
        "#bcf60c",
        "#fabebe",
        "#008080",
        "#9a6324",
        "#800000",
    ]

    net = Network(
        height="800px",
        width="100%",
        bgcolor="#111",
        font_color="#eee",
        notebook=False,
        directed=False,
    )
    net.barnes_hut(gravity=-8000, central_gravity=0.3, spring_length=120)

    for n, data in G.nodes(data=True):
        ci = node_comm.get(n, 0)
        deg = G.degree(n)
        label = data.get("label", n)
        etype = data.get("entity_type", "concept")
        net.add_node(
            n,
            label=label if deg > 2 else "",  # only label hubs, keep it readable
            title=f"{label}\ntype: {etype}\ndegree: {deg}",
            color=palette[ci % len(palette)],
            size=8 + 3 * deg,
        )
    for u, v, data in G.edges(data=True):
        net.add_edge(u, v, title=data.get("edge_type", ""), color="#555")

    # Homology + structure summary panel
    h1 = homology_summary.get("h1_features", "?")
    h1p = homology_summary.get("h1_persistent", "?")
    n_comp = nx.number_connected_components(G) if len(G) else 0
    heading = (
        f"<div style='position:fixed;top:8px;left:8px;z-index:999;"
        f"background:#1c1c1c;color:#eee;padding:10px 14px;border-radius:8px;"
        f"font-family:monospace;font-size:13px;line-height:1.5'>"
        f"<b>good-dog knowledge graph</b><br>"
        f"nodes {G.number_of_nodes()} &middot; edges {G.number_of_edges()} "
        f"&middot; communities {len(comms)}<br>"
        f"<b>topology:</b> H0 (components) {n_comp} &middot; "
        f"H1 (loops) {h1} &middot; persistent loops {h1p}<br>"
        f"<span style='color:#888'>H1 loops = independent cycles: ideas connected "
        f"by more than one path (real structure, not a tree)</span>"
        f"</div>"
    )
    net.write_html(out_path, notebook=False)
    # Inject the summary panel
    html = Path(out_path).read_text()
    html = html.replace("<body>", f"<body>{heading}", 1)
    Path(out_path).write_text(html)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph", default="data/graph.lbug")
    ap.add_argument("--out", default="graph.html")
    args = ap.parse_args()

    print(f"Loading graph from {args.graph} (native get_as_networkx)...")
    G = load_graph_native(args.graph)
    print(f"  {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

    print("Computing persistent homology (Ripser)...")
    hsum = homology(G)
    if hsum.get("available"):
        print(
            f"  H0={hsum.get('h0_features')}  H1={hsum.get('h1_features')}  "
            f"persistent H1={hsum.get('h1_persistent')}"
        )
    else:
        print(f"  homology unavailable: {hsum.get('reason')}")

    print(f"Rendering → {args.out}")
    render(G, hsum, args.out)
    print(f"Done. Open {args.out} in a browser.")


if __name__ == "__main__":
    main()
