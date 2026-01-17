"""Floyd-Warshall (equação de Floyd) para todos os pares.

Enunciado da simulação 3:
- Grafo direcionado com circuitos e custos negativos
- Representação: matriz de adjacência/custos
- Computar caminho mínimo de X1 para todos os outros pela primeira linha da matriz final

Aqui implementamos a forma clássica O(n^3) com matriz de predecessores para reconstrução.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np


@dataclass
class FloydStats:
    iterations: int = 0
    relaxations: int = 0
    negative_cycle: bool = False


def floyd_warshall(cost_matrix: np.ndarray) -> tuple[np.ndarray, np.ndarray, FloydStats]:
    """Retorna (dist, nxt, stats).

    - dist: matriz de distâncias mínimas
    - nxt: matriz de próximos nós para reconstrução de caminho (i->j)

    Se não existe caminho i->j, nxt[i,j] = -1.
    """
    n = cost_matrix.shape[0]
    dist = cost_matrix.astype(float).copy()

    nxt = np.full((n, n), -1, dtype=int)
    for i in range(n):
        for j in range(n):
            if i != j and np.isfinite(dist[i, j]):
                nxt[i, j] = j

    stats = FloydStats()

    for k in range(n):
        for i in range(n):
            dik = dist[i, k]
            if not np.isfinite(dik):
                continue
            for j in range(n):
                stats.iterations += 1
                dkj = dist[k, j]
                if not np.isfinite(dkj):
                    continue
                nd = dik + dkj
                if nd < dist[i, j]:
                    dist[i, j] = nd
                    nxt[i, j] = nxt[i, k]
                    stats.relaxations += 1

    # Ciclo negativo: dist[i,i] < 0
    stats.negative_cycle = bool(np.any(np.diag(dist) < 0))

    return dist, nxt, stats


def reconstruct_path(nxt: np.ndarray, i: int, j: int) -> list[int]:
    """Reconstrói o caminho i->j usando a matriz nxt."""
    # Caso base: caminho trivial do nó para ele mesmo.
    if i == j:
        return [int(i)]
    if nxt[i, j] == -1:
        return []
    path = [i]
    while i != j:
        i = int(nxt[i, j])
        if i == -1:
            return []
        path.append(i)
        if len(path) > nxt.shape[0] + 5:
            # segurança contra loop inesperado
            return []
    return path
