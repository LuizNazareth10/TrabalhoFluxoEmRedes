"""Visualizador de grafos gerados nas simulações.

Uso:
    python -m fluxo_redes.visualize --graph results/sim1_Bellman_n10_graph.json --out figures/sim1_Bellman_n10_viz.png
"""

from __future__ import annotations

import argparse
import json
import os
from typing import Tuple

import matplotlib.pyplot as plt
import networkx as nx


def _vertex_label(i: int) -> str:
    return f"X{i+1}"


def _default_out_path(graph_path: str) -> str:
    base, _ = os.path.splitext(graph_path)
    return base + "_viz.png"


def _layout_positions(G: nx.DiGraph, layout: str, seed: int | None) -> dict:
    if layout == "spring":
        return nx.spring_layout(G, seed=seed)
    if layout == "kamada":
        return nx.kamada_kawai_layout(G)
    if layout == "circular":
        return nx.circular_layout(G)
    raise ValueError("layout deve ser spring, kamada ou circular")


def draw_graph(
    graph_path: str,
    out_path: str,
    layout: str = "spring",
    seed: int | None = 42,
    with_labels: bool = True,
    with_edge_labels: bool = True,
    node_size: int = 700,
    font_size: int = 9,
) -> None:
    with open(graph_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    n = int(data["n"])
    edges = data["edges"]

    G = nx.DiGraph()
    for i in range(n):
        G.add_node(i)
    for e in edges:
        G.add_edge(int(e["u"]), int(e["v"]), weight=float(e["w"]))

    pos = _layout_positions(G, layout, seed)

    neg_edges = [(u, v) for u, v, w in G.edges(data="weight") if w < 0]
    pos_edges = [(u, v) for u, v, w in G.edges(data="weight") if w >= 0]

    plt.figure(figsize=(10, 7))

    nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color="#93C5FD", edgecolors="#1D4ED8")
    nx.draw_networkx_edges(G, pos, edgelist=pos_edges, edge_color="#6B7280", arrows=True, arrowsize=12, width=1.2)
    if neg_edges:
        nx.draw_networkx_edges(G, pos, edgelist=neg_edges, edge_color="#EF4444", arrows=True, arrowsize=12, width=1.5)

    if with_labels:
        labels = {i: _vertex_label(i) for i in range(n)}
        nx.draw_networkx_labels(G, pos, labels=labels, font_size=font_size)

    if with_edge_labels:
        edge_labels = {(u, v): f"{d['weight']}" for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=max(7, font_size - 2))

    title = f"Simulação {data.get('sim_id', '')} — {data.get('sim_name', '')} | n={n}"
    plt.title(title)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(out_path, dpi=160)
    plt.close()


def main() -> int:
    ap = argparse.ArgumentParser(description="Visualiza um grafo gerado nas simulações")
    ap.add_argument("--graph", type=str, required=True, help="Arquivo .json do grafo")
    ap.add_argument("--out", type=str, help="Arquivo de saída (png)")
    ap.add_argument("--layout", type=str, default="spring", choices=["spring", "kamada", "circular"], help="Layout do grafo")
    ap.add_argument("--seed", type=int, default=42, help="Seed do layout (spring)")
    ap.add_argument("--no-labels", action="store_true", help="Não desenhar rótulos de vértices")
    ap.add_argument("--no-edge-labels", action="store_true", help="Não desenhar pesos nas arestas")
    args = ap.parse_args()

    out_path = args.out or _default_out_path(args.graph)

    draw_graph(
        graph_path=args.graph,
        out_path=out_path,
        layout=args.layout,
        seed=args.seed,
        with_labels=not args.no_labels,
        with_edge_labels=not args.no_edge_labels,
    )

    print(f"Figura gerada: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
