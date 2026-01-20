"""CLI para rodar as 3 simulações e gerar resultados.

Uso:
    python -m fluxo_redes.simulations --all --sizes 10 100 --out results

Principais saídas:
- results/run_manifest.json
- results/summary.csv
- results/<sim>_<n>_distances.csv
- results/<sim>_<n>_graph.json
- figures/<sim>_<n>_<...>.png
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime
from time import perf_counter
from typing import Optional, Dict, Any, List

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from .graph_generators import (
    generate_dag_negative_costs,
    generate_cyclic_nonnegative,
    generate_cyclic_with_negative_no_neg_cycles,
    edge_stats,
)
from .representations import (
    to_predecessor_list,
    to_successor_list,
    to_cost_matrix,
    edges_to_jsonable,
)
from .utils import reconstruct_path_from_predecessor
from .algorithms.bellman_divide_conquer import shortest_paths_bellman_dag_recursive
from .algorithms.dijkstra_heap import dijkstra_heap
from .algorithms.floyd_warshall import floyd_warshall, reconstruct_path


def _vertex_label(i: int) -> str:
    return f"X{i+1}"


def _sim_name(sim_id: int) -> str:
    if sim_id == 1:
        return "Bellman"
    if sim_id == 2:
        return "Dijkstra"
    if sim_id == 3:
        return "Floyd"
    raise ValueError("sim_id deve ser 1, 2 ou 3")


def _distance_stats(dist: List[float]) -> dict:
    arr = np.array(dist, dtype=float)
    finite = arr[np.isfinite(arr)]
    if finite.size == 0:
        return {"reachable": 0, "min": None, "max": None, "mean": None, "std": None}
    return {
        "reachable": int(finite.size),
        "min": float(finite.min()),
        "max": float(finite.max()),
        "mean": float(finite.mean()),
        "std": float(finite.std(ddof=0)),
    }


def _save_plot_distance_hist(dist: List[float], outpath: str, title: str) -> None:
    arr = np.array(dist, dtype=float)
    finite = arr[np.isfinite(arr)]
    plt.figure()
    if finite.size > 0:
        plt.hist(finite, bins=min(30, max(5, int(np.sqrt(finite.size)))))
    plt.title(title)
    plt.xlabel("Distância a partir de X1")
    plt.ylabel("Frequência")
    plt.tight_layout()
    plt.savefig(outpath, dpi=150)
    plt.close()


def _save_plot_distance_by_vertex(dist: List[float], outpath: str, title: str) -> None:
    arr = np.array(dist, dtype=float)
    x = np.arange(len(arr)) + 1
    plt.figure()
    plt.plot(x, arr)
    plt.title(title)
    plt.xlabel("Índice do vértice (1..n)")
    plt.ylabel("Distância a partir de X1")
    plt.tight_layout()
    plt.savefig(outpath, dpi=150)
    plt.close()


def _format_predecessor_list(preds: List[List[tuple[int, float]]]) -> str:
    lines: List[str] = []
    for v, items in enumerate(preds):
        label_v = _vertex_label(v)
        if not items:
            lines.append(f"{label_v}: []")
            continue
        parts = [f"({_vertex_label(u)}, {w})" for (u, w) in items]
        lines.append(f"{label_v}: [" + ", ".join(parts) + "]")
    return "\n".join(lines)


def _format_successor_list(succs: List[List[tuple[int, float]]]) -> str:
    lines: List[str] = []
    for u, items in enumerate(succs):
        label_u = _vertex_label(u)
        if not items:
            lines.append(f"{label_u}: []")
            continue
        parts = [f"({_vertex_label(v)}, {w})" for (v, w) in items]
        lines.append(f"{label_u}: [" + ", ".join(parts) + "]")
    return "\n".join(lines)


def _format_cost_matrix(mat: np.ndarray) -> str:
    lines: List[str] = []
    n = mat.shape[0]
    header = [" "] + [_vertex_label(i) for i in range(n)]
    lines.append("\t".join(header))
    for i in range(n):
        row = [_vertex_label(i)]
        for j in range(n):
            val = mat[i, j]
            row.append("INF" if not np.isfinite(val) else f"{float(val)}")
        lines.append("\t".join(row))
    return "\n".join(lines)


def run_simulation(sim_id: int, n: int, density: float, seed: int, out_dir: str, fig_dir: str) -> Dict[str, Any]:
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(fig_dir, exist_ok=True)
    graphs_dir = os.path.join(out_dir, "graphs")
    os.makedirs(graphs_dir, exist_ok=True)
    sim_name = _sim_name(sim_id)

    if sim_id == 1:
        edges = generate_dag_negative_costs(n=n, density=density, seed=seed)
        preds = to_predecessor_list(n, edges)
        succs = to_successor_list(n, edges)
        mat = to_cost_matrix(n, edges)
        t0 = perf_counter()
        dist, pred, stats_alg = shortest_paths_bellman_dag_recursive(preds, root=0)
        t1 = perf_counter()
        alg_extra = {
            "recursion_calls": stats_alg.recursion_calls,
            "relax_checks": stats_alg.relax_checks,
        }
        # path via predecessor
        paths = [reconstruct_path_from_predecessor(pred, v, root=0) for v in range(n)]

    elif sim_id == 2:
        edges = generate_cyclic_nonnegative(n=n, density=density, seed=seed)
        succs = to_successor_list(n, edges)
        preds = to_predecessor_list(n, edges)
        mat = to_cost_matrix(n, edges)
        t0 = perf_counter()
        dist, pred, stats_alg = dijkstra_heap(succs, root=0)
        t1 = perf_counter()
        alg_extra = {
            "relaxations": stats_alg.relaxations,
            "heap_push": stats_alg.heap_push,
            "heap_pop": stats_alg.heap_pop,
        }
        paths = [reconstruct_path_from_predecessor(pred, v, root=0) for v in range(n)]

    elif sim_id == 3:
        edges = generate_cyclic_with_negative_no_neg_cycles(n=n, density=density, seed=seed)
        mat = to_cost_matrix(n, edges)
        preds = to_predecessor_list(n, edges)
        succs = to_successor_list(n, edges)
        t0 = perf_counter()
        dist_mat, nxt, stats_alg = floyd_warshall(mat)
        t1 = perf_counter()
        dist = dist_mat[0, :].tolist()  # primeira linha
        pred = [None] * n  # não é predecessor; mantemos None
        alg_extra = {
            "iterations": stats_alg.iterations,
            "relaxations": stats_alg.relaxations,
            "negative_cycle": bool(stats_alg.negative_cycle),
        }
        paths = [reconstruct_path(nxt, 0, v) for v in range(n)]

    else:
        raise ValueError("sim_id deve ser 1, 2 ou 3")

    runtime_s = float(t1 - t0)

    # salva grafo
    graph_path = os.path.join(out_dir, f"sim{sim_id}_{sim_name}_n{n}_graph.json")
    with open(graph_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "sim_id": sim_id,
                "sim_name": sim_name,
                "n": n,
                "density": density,
                "seed": seed,
                "edges": edges_to_jsonable(edges),
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

    # salva grafo em txt descritivo para uso em LLM (todas as representações)
    graph_txt_path = os.path.join(graphs_dir, f"sim{sim_id}_{sim_name}_n{n}_graph.txt")
    with open(graph_txt_path, "w", encoding="utf-8") as f:
        f.write(f"sim_id={sim_id}\n")
        f.write(f"sim_name={sim_name}\n")
        f.write(f"n={n}\n")
        f.write(f"density={density}\n")
        f.write(f"seed={seed}\n")
        f.write("\n")
        f.write("LISTA DE ANTECESSORES\n")
        f.write("\n")
        f.write(_format_predecessor_list(preds))
        f.write("\n\n")
        f.write("LISTA DE SUCESSORES\n")
        f.write("\n")
        f.write(_format_successor_list(succs))
        f.write("\n\n")
        f.write("MATRIZ DE CUSTOS\n")
        f.write("\n")
        f.write(_format_cost_matrix(mat))

    # tabela de distâncias
    rows = []
    for v in range(n):
        p = paths[v]
        rows.append(
            {
                "vertex": v,
                "label": _vertex_label(v),
                "distance": float(dist[v]) if np.isfinite(dist[v]) else float("inf"),
                "reachable": bool(np.isfinite(dist[v])),
                "path": " -> ".join(_vertex_label(x) for x in p) if p else "",
                "path_hops": int(len(p) - 1) if p else None,
                "predecessor": _vertex_label(pred[v]) if pred[v] is not None else "",
            }
        )
    df_dist = pd.DataFrame(rows)
    dist_path = os.path.join(out_dir, f"sim{sim_id}_{sim_name}_n{n}_distances.csv")
    df_dist.to_csv(dist_path, index=False, encoding="utf-8")

    # figuras
    _save_plot_distance_hist(dist, os.path.join(fig_dir, f"sim{sim_id}_{sim_name}_n{n}_hist.png"), f"Sim {sim_id} ({sim_name}) | n={n} | Histograma")
    _save_plot_distance_by_vertex(dist, os.path.join(fig_dir, f"sim{sim_id}_{sim_name}_n{n}_series.png"), f"Sim {sim_id} ({sim_name}) | n={n} | Distância por vértice")

    # resumo
    e_stats = edge_stats(edges)
    d_stats = _distance_stats(dist)

    summary = {
        "sim_id": sim_id,
        "sim_name": sim_name,
        "n": n,
        "density": density,
        "seed": seed,
        "runtime_s": runtime_s,
        **e_stats,
        **{f"dist_{k}": v for k, v in d_stats.items()},
        **{f"alg_{k}": v for k, v in alg_extra.items()},
        "graph_file": os.path.basename(graph_path),
        "dist_file": os.path.basename(dist_path),
    }
    return summary


def main() -> int:
    ap = argparse.ArgumentParser(description="Roda as simulações do trabalho de Fluxo em Redes")
    ap.add_argument("--sim", type=int, choices=[1, 2, 3], help="Rodar apenas uma simulação")
    ap.add_argument("--all", action="store_true", help="Rodar as 3 simulações")
    ap.add_argument("--sizes", type=int, nargs="+", default=[10, 100], help="Tamanhos n")
    ap.add_argument("--density", type=float, default=0.25, help="Densidade aproximada de arestas")
    ap.add_argument("--seed", type=int, default=42, help="Seed")
    ap.add_argument("--out", type=str, default="results", help="Pasta de resultados")
    ap.add_argument("--figures", type=str, default="figures", help="Pasta de figuras")

    args = ap.parse_args()

    sims = []
    if args.all:
        sims = [1, 2, 3]
    elif args.sim:
        sims = [args.sim]
    else:
        ap.error("Use --all ou --sim")

    out_dir = args.out
    fig_dir = args.figures
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(fig_dir, exist_ok=True)

    manifest = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "command": " ".join(os.sys.argv),
        "sims": sims,
        "sizes": args.sizes,
        "density": args.density,
        "seed": args.seed,
    }
    with open(os.path.join(out_dir, "run_manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    summaries = []
    for sim_id in sims:
        for n in args.sizes:
            # usa seed deslocada por sim e n para variar, mantendo reprodutível
            seed = int(args.seed + 1000 * sim_id + n)
            summaries.append(run_simulation(sim_id, n, args.density, seed, out_dir, fig_dir))

    df_sum = pd.DataFrame(summaries)
    df_sum.to_csv(os.path.join(out_dir, "summary.csv"), index=False, encoding="utf-8")

    print(df_sum[["sim_id", "n", "runtime_s", "m", "neg_edges", "dist_reachable", "dist_mean"]].to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
