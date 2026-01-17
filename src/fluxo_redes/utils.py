"""Utilidades gerais."""

from __future__ import annotations

from typing import List, Optional


def reconstruct_path_from_predecessor(pred: List[Optional[int]], target: int, root: int = 0) -> List[int]:
    """Reconstrói caminho root->target dado vetor predecessor (prev/parent).

    Retorna lista de nós (índices). Se inalcançável, retorna [].
    """
    if target == root:
        return [root]

    path = []
    cur = target
    seen = set()
    while cur is not None:
        if cur in seen:
            # segurança contra ciclo no vetor predecessor
            return []
        seen.add(cur)
        path.append(cur)
        if cur == root:
            break
        cur = pred[cur]

    if not path or path[-1] != root:
        return []
    path.reverse()
    return path
