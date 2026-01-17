"""Parte 2 do enunciado: resolver usando linguagem generativa.

Como este projeto precisa rodar offline, incluímos:
1) Geradores de prompts (um para cada representação).
2) Um modo `--demo` que:
   - carrega um grafo salvo em results/
   - imprime o prompt
   - executa um *mock* que devolve as distâncias usando nossos algoritmos (serve para validar o formato de entrada/saída).

Opcional: você pode plugar uma API de LLM real.
- Por padrão, o código NÃO chama internet.
- Se você quiser, edite `call_llm_real()` para sua API favorita.

Importante: o enunciado pede que o prompt solicite apenas "computar o caminho mínimo".
Este arquivo já gera prompts com esse cuidado.
"""

from __future__ import annotations

import argparse
import json
import os
from typing import List, Tuple

import numpy as np

from .representations import to_predecessor_list, to_successor_list, to_cost_matrix
from .graph_generators import Edge
from .algorithms.bellman_divide_conquer import shortest_paths_bellman_dag_recursive
from .algorithms.dijkstra_heap import dijkstra_heap
from .algorithms.floyd_warshall import floyd_warshall


def _vertex_label(i: int) -> str:
    return f"X{i+1}"


def prompt_sim1(predecessors: List[List[Tuple[int, float]]]) -> str:
    lines = []
    lines.append(
        "Dado um grafo direcionado com vértices X1..Xn e a seguinte lista de antecessores "
        "(para cada Xi: lista de (Xj, custo Xj->Xi)), calcule APENAS o custo do caminho mínimo de X1 até todos os demais vértices.\n"
        "Devolva uma lista de n valores d(X1), d(X2), ..., d(Xn). (sem explicações adicionais)\n\n"
        "ENTRADA:"
    )
    for v, preds in enumerate(predecessors):
        s = ", ".join(f"({_vertex_label(u)}, {w})" for (u, w) in preds)
        lines.append(f"{_vertex_label(v)}: [{s}]")
    return "\n".join(lines)


def prompt_sim2(successors: List[List[Tuple[int, float]]]) -> str:
    lines = []
    lines.append(
        "Dado um grafo direcionado com vértices X1..Xn e a seguinte lista de sucessores "
        "(para cada Xi: lista de (Xj, custo Xi->Xj)), calcule APENAS o custo do caminho mínimo de X1 até todos os demais vértices.\n"
        "Devolva uma lista de n valores d(X1), d(X2), ..., d(Xn). (sem explicações adicionais)\n\n"
        "ENTRADA:"
    )
    for u, succs in enumerate(successors):
        s = ", ".join(f"({_vertex_label(v)}, {w})" for (v, w) in succs)
        lines.append(f"{_vertex_label(u)}: [{s}]")
    return "\n".join(lines)


def prompt_sim3(cost_matrix: np.ndarray) -> str:
    # imprime matriz compacta (pode ficar grande para n=100; no demo usamos n=10)
    lines = []
    lines.append(
        "Dado um grafo direcionado com vértices X1..Xn e a seguinte matriz de custos C "
        "(C[i][j] = custo Xi->Xj; use INF quando não existir arco), calcule APENAS o custo do caminho mínimo de X1 até todos os demais vértices.\n"
        "Devolva a primeira linha da matriz final de distâncias (d(X1->X1)..d(X1->Xn)). (sem explicações adicionais)\n\n"
        "ENTRADA (matriz C):"
    )
    for i in range(cost_matrix.shape[0]):
        row = []
        for j in range(cost_matrix.shape[1]):
            val = cost_matrix[i, j]
            row.append("INF" if not np.isfinite(val) else f"{val:.0f}")
        lines.append("[" + ", ".join(row) + "]")
    return "\n".join(lines)


def _load_graph(graph_json_path: str) -> tuple[int, List[Edge]]:
    with open(graph_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    n = int(data["n"])
    edges = [Edge(int(e["u"]), int(e["v"]), float(e["w"])) for e in data["edges"]]
    return n, edges


def run_demo(results_dir: str, sim_id: int, n: int) -> None:
    graph_json = os.path.join(results_dir, f"sim{sim_id}_n{n}_graph.json")
    if not os.path.exists(graph_json):
        raise FileNotFoundError(f"Não encontrei {graph_json}. Rode as simulações primeiro.")

    n_loaded, edges = _load_graph(graph_json)
    assert n_loaded == n

    if sim_id == 1:
        preds = to_predecessor_list(n, edges)
        prompt = prompt_sim1(preds)
        dist, _, _ = shortest_paths_bellman_dag_recursive(preds, root=0)
        answer = dist
    elif sim_id == 2:
        succs = to_successor_list(n, edges)
        prompt = prompt_sim2(succs)
        dist, _, _ = dijkstra_heap(succs, root=0)
        answer = dist
    else:
        mat = to_cost_matrix(n, edges)
        prompt = prompt_sim3(mat)
        dist_mat, _, _ = floyd_warshall(mat)
        answer = dist_mat[0, :].tolist()

    print("\n===== PROMPT =====\n")
    print(prompt)
    print("\n===== RESPOSTA (MOCK) =====\n")
    print([float(x) if np.isfinite(x) else float("inf") for x in answer])


def main() -> int:
    ap = argparse.ArgumentParser(description="Parte 2: prompts de linguagem generativa")
    ap.add_argument("--demo", action="store_true", help="Roda demo offline (mock)")
    ap.add_argument("--results", type=str, default="results", help="Pasta results")
    ap.add_argument("--sim", type=int, choices=[1, 2, 3], default=1)
    ap.add_argument("--n", type=int, default=10)
    args = ap.parse_args()

    if args.demo:
        run_demo(args.results, args.sim, args.n)
        return 0

    print("Use --demo para demonstrar (offline). Para integrar uma API real, edite este módulo.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
