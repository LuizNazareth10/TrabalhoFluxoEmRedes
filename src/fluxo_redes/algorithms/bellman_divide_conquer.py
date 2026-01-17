"""Bellman (DAG) com implementação recursiva (divisão e conquista).

Para um DAG, o caminho mínimo da raiz 0 para v pode ser calculado pela
recorrência de Bellman:

    d(0) = 0
    d(v) = min_{(u->v)} d(u) + w(u,v)

Em um DAG, esta recorrência é bem-definida. Aqui implementamos uma versão
recursiva em que d(v) chama d(u) para seus antecessores.

Para evitar recomputação exponencial, usamos memoização.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple, Optional


@dataclass
class BellmanRecStats:
    recursion_calls: int = 0
    relax_checks: int = 0


def shortest_paths_bellman_dag_recursive(
    predecessors: List[List[Tuple[int, float]]],
    root: int = 0,
) -> tuple[list[float], list[Optional[int]], BellmanRecStats]:
    """Retorna distâncias e predecessores do caminho mínimo a partir de root.

    predecessors[v] = lista de (u, w(u,v)).

    Se v for inalcançável, d(v)=inf e pred[v]=None.
    """
    n = len(predecessors)
    INF = float("inf")

    memo: List[Optional[float]] = [None] * n
    pred: List[Optional[int]] = [None] * n
    in_stack = [False] * n  # segurança: detecta ciclo acidental

    stats = BellmanRecStats()

    def solve(v: int) -> float:
        stats.recursion_calls += 1
        if memo[v] is not None:
            return memo[v]
        if v == root:
            memo[v] = 0.0
            pred[v] = None
            return 0.0
        if in_stack[v]:
            # Se ocorrer, o grafo não é DAG (contraria o enunciado da simulação 1).
            raise ValueError("Ciclo detectado na recursão; grafo não é DAG")

        in_stack[v] = True

        best = INF
        best_u: Optional[int] = None
        for (u, w) in predecessors[v]:
            stats.relax_checks += 1
            du = solve(u)
            if du == INF:
                continue
            cand = du + w
            if cand < best:
                best = cand
                best_u = u

        in_stack[v] = False
        memo[v] = best
        pred[v] = best_u
        return best

    dists: List[float] = [INF] * n
    for v in range(n):
        dists[v] = solve(v)

    return dists, pred, stats
