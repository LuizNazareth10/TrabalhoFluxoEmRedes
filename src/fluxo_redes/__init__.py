"""Fluxo em Redes — Caminho Mínimo.

Implementa as 3 simulações do enunciado:
1) Bellman recursivo em DAG com custos negativos (lista de antecessores)
2) Dijkstra com heap em grafo com ciclos e custos não-negativos (lista de sucessores)
3) Floyd-Warshall em grafo com ciclos e custos negativos (matriz de custos)

O ponto de entrada recomendado é via CLI:
- python -m fluxo_redes.simulations
- python -m fluxo_redes.report
"""

__all__ = ["graph_generators", "representations", "simulations", "report"]
