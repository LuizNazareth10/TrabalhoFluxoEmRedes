"""Dijkstra (Best-First) usando Heap para lista de abertos.

Enunciado da simulação 2:
- Grafo direcionado com circuitos, sem custos negativos
- Representação: lista de sucessores
- Implementação: Best-First / busca ordenada com Heap

Esta implementação é a forma canônica do Dijkstra com fila de prioridade.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple, Optional
import heapq


@dataclass
class DijkstraStats:
    relaxations: int = 0
    heap_push: int = 0
    heap_pop: int = 0


def dijkstra_heap(
    successors: List[List[Tuple[int, float]]],
    root: int = 0,
) -> tuple[list[float], list[Optional[int]], DijkstraStats]:
    n = len(successors)
    INF = float("inf")

    dist = [INF] * n
    prev: List[Optional[int]] = [None] * n
    dist[root] = 0.0

    stats = DijkstraStats()

    heap: List[Tuple[float, int]] = [(0.0, root)]
    stats.heap_push += 1

    visited = [False] * n

    while heap:
        d_u, u = heapq.heappop(heap)
        stats.heap_pop += 1

        if visited[u]:
            continue
        visited[u] = True

        if d_u > dist[u]:
            continue

        for v, w in successors[u]:
            if w < 0:
                raise ValueError("Dijkstra requer pesos não-negativos")
            nd = d_u + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(heap, (nd, v))
                stats.heap_push += 1
                stats.relaxations += 1

    return dist, prev, stats
