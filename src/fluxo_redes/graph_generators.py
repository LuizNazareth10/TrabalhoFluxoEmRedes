"""Geração de grafos para as 3 simulações.

O enunciado recomenda grafos densos e sem laços.
Este módulo fornece geradores reprodutíveis (via seed) que respeitam
as restrições de cada simulação.

Representação interna: lista de arestas (u, v, w) com vértices 0..n-1.
X1 corresponde ao índice 0.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple, Optional

import numpy as np


@dataclass(frozen=True)
class Edge:
    """Aresta direcionada u->v com custo w."""

    u: int
    v: int
    w: float


def _dedup_edges(edges: List[Edge]) -> List[Edge]:
    """Remove duplicatas (mantendo a última ocorrência) e garante ausência de laços."""
    m = {}
    for e in edges:
        if e.u == e.v:
            continue
        m[(e.u, e.v)] = e
    return list(m.values())


def generate_dag_negative_costs(
    n: int,
    density: float,
    seed: Optional[int] = None,
    neg_fraction: float = 0.35,
    weight_range: Tuple[int, int] = (1, 20),
) -> List[Edge]:
    """Gera um DAG denso (arestas só i->j para i<j) com custos negativos permitidos."""
    rng = np.random.default_rng(seed)
    edges: List[Edge] = []

    # Corrente base para garantir alcançabilidade a partir de X1.
    for i in range(n - 1):
        w = int(rng.integers(weight_range[0], weight_range[1] + 1))
        # Permite negativo na corrente também.
        if rng.random() < neg_fraction:
            w = -w
        edges.append(Edge(i, i + 1, float(w)))

    # Arestas adicionais i<j (sem ciclos).
    for i in range(n):
        for j in range(i + 1, n):
            if j == i + 1:
                continue
            if rng.random() < density:
                w = int(rng.integers(weight_range[0], weight_range[1] + 1))
                if rng.random() < neg_fraction:
                    w = -w
                edges.append(Edge(i, j, float(w)))

    return _dedup_edges(edges)


def generate_cyclic_nonnegative(
    n: int,
    density: float,
    seed: Optional[int] = None,
    weight_range: Tuple[int, int] = (1, 30),
) -> List[Edge]:
    """Gera um grafo direcionado com ciclos e pesos não-negativos (Dijkstra)."""
    rng = np.random.default_rng(seed)
    edges: List[Edge] = []

    # Garante alcançabilidade via corrente.
    for i in range(n - 1):
        w = int(rng.integers(weight_range[0], weight_range[1] + 1))
        edges.append(Edge(i, i + 1, float(w)))

    # Arestas aleatórias em todas as direções (exceto laços).
    for u in range(n):
        for v in range(n):
            if u == v:
                continue
            # evita re-inserir a corrente com muita frequência
            if v == u + 1:
                continue
            if rng.random() < density:
                w = int(rng.integers(weight_range[0], weight_range[1] + 1))
                edges.append(Edge(u, v, float(w)))

    return _dedup_edges(edges)


def generate_cyclic_with_negative_no_neg_cycles(
    n: int,
    density: float,
    seed: Optional[int] = None,
    base_range: Tuple[int, int] = (1, 25),
    potential_range: Tuple[int, int] = (-20, 20),
) -> List[Edge]:
    """Gera grafo com ciclos e custos negativos, mas sem ciclos negativos.

    Truque: gera custos base não-negativos b(u,v) >= 1 e potenciais pi[i].
    Define w(u,v) = b(u,v) + pi[v] - pi[u].

    Para qualquer ciclo, a soma de (pi[v]-pi[u]) cancela, restando soma de b >= 0.
    Logo, não existem ciclos negativos, embora possam existir arestas negativas.
    """
    rng = np.random.default_rng(seed)
    pi = rng.integers(potential_range[0], potential_range[1] + 1, size=n)

    edges: List[Edge] = []

    # Corrente base para alcançabilidade.
    for i in range(n - 1):
        b = int(rng.integers(base_range[0], base_range[1] + 1))
        w = b + int(pi[i + 1]) - int(pi[i])
        edges.append(Edge(i, i + 1, float(w)))

    for u in range(n):
        for v in range(n):
            if u == v:
                continue
            if v == u + 1:
                continue
            if rng.random() < density:
                b = int(rng.integers(base_range[0], base_range[1] + 1))
                w = b + int(pi[v]) - int(pi[u])
                edges.append(Edge(u, v, float(w)))

    return _dedup_edges(edges)


def edge_stats(edges: List[Edge]) -> dict:
    """Resumo simples de estatísticas de arestas."""
    if not edges:
        return {"m": 0, "neg_edges": 0, "min_w": None, "max_w": None, "avg_w": None}

    ws = np.array([e.w for e in edges], dtype=float)
    return {
        "m": int(len(edges)),
        "neg_edges": int(np.sum(ws < 0.0)),
        "min_w": float(ws.min()),
        "max_w": float(ws.max()),
        "avg_w": float(ws.mean()),
    }
