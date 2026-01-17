"""Conversões entre representações.

O trabalho exige:
- Simulação 1: lista de antecessores
- Simulação 2: lista de sucessores
- Simulação 3: matriz de custos

Este módulo converte uma lista de arestas (u,v,w) para cada representação.
"""

from __future__ import annotations

from typing import List, Tuple

import numpy as np

from .graph_generators import Edge


def to_predecessor_list(n: int, edges: List[Edge]) -> List[List[Tuple[int, float]]]:
    preds: List[List[Tuple[int, float]]] = [[] for _ in range(n)]
    for e in edges:
        preds[e.v].append((e.u, float(e.w)))
    return preds


def to_successor_list(n: int, edges: List[Edge]) -> List[List[Tuple[int, float]]]:
    succs: List[List[Tuple[int, float]]] = [[] for _ in range(n)]
    for e in edges:
        succs[e.u].append((e.v, float(e.w)))
    return succs


def to_cost_matrix(n: int, edges: List[Edge], inf: float = float("inf")) -> np.ndarray:
    mat = np.full((n, n), inf, dtype=float)
    np.fill_diagonal(mat, 0.0)
    for e in edges:
        mat[e.u, e.v] = float(e.w)
    return mat


def edges_to_jsonable(edges: List[Edge]) -> List[dict]:
    return [{"u": e.u, "v": e.v, "w": float(e.w)} for e in edges]
