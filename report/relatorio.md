# Relatório — Fluxo em Redes (Caminho Mínimo)

Gerado em 2026-01-20T18:36:56.951589Z

## Visão geral

O projeto implementa três simulações de caminho mínimo a partir da raiz X1, com diferentes hipóteses sobre ciclos e sinais dos custos, e com representações distintas de grafo.

### Resumo executivo dos resultados

| sim_id | sim_name | n   | m    | neg_edges | runtime_s | dist_reachable | dist_min  | dist_mean | dist_max |
| ------ | -------- | --- | ---- | --------- | --------- | -------------- | --------- | --------- | -------- |
| 1      | Bellman  | 10  | 22   | 7         | 0.0000    | 10             | -48.0000  | -6.3000   | 39.0000  |
| 1      | Bellman  | 100 | 1307 | 462       | 0.0004    | 100            | -295.0000 | -126.2400 | 50.0000  |
| 2      | Dijkstra | 10  | 25   | 0         | 0.0000    | 10             | 0.0000    | 24.0000   | 53.0000  |
| 2      | Dijkstra | 100 | 2549 | 0         | 0.0003    | 100            | 0.0000    | 6.7000    | 12.0000  |
| 3      | Floyd    | 10  | 32   | 9         | 0.0014    | 10             | 0.0000    | 24.6000   | 50.0000  |
| 3      | Floyd    | 100 | 2499 | 564       | 0.7642    | 100            | -20.0000  | 0.7700    | 20.0000  |

## Simulação 1 — Bellman recursivo em DAG com custos negativos (lista de antecessores)

**Ponto-chave:** como o grafo não possui circuitos, a recorrência de Bellman é bem definida e pode ser avaliada recursivamente. A memoização é essencial para evitar recomputações.

### Execução: n=10

- Arestas (m): 22 | densidade efetiva: 0.244 | arestas negativas: 7

- Alcançáveis a partir de X1: 10/10 (inalcançáveis: 0)

- Tempo de execução: 0.000020 s

- Contadores internos: heap_pop=nan, heap_push=nan, iterations=nan, negative_cycle=nan, recursion_calls=32.0, relax_checks=22.0, relaxations=nan

- Hops (arestas no caminho): min=0 | média=2.30 | max=5 | desvio=1.42

- Indicador de espalhamento (dist_max / dist_mean): -6.19. Valores mais altos sugerem maior heterogeneidade entre caminhos curtos e longos.

#### Ranking de distância (mais perto → mais longe)

| label | distance | path                              |
| ----- | -------- | --------------------------------- |
| X8    | -48.0000 | X1 -> X6 -> X7 -> X8              |
| X10   | -47.0000 | X1 -> X6 -> X7 -> X8 -> X9 -> X10 |
| X9    | -44.0000 | X1 -> X6 -> X7 -> X8 -> X9        |
| X7    | -30.0000 | X1 -> X6 -> X7                    |
| X6    | -17.0000 | X1 -> X6                          |
| X1    | 0.0000   | X1                                |
| X2    | 20.0000  | X1 -> X2                          |
| X5    | 27.0000  | X1 -> X2 -> X5                    |
| X4    | 37.0000  | X1 -> X2 -> X3 -> X4              |
| X3    | 39.0000  | X1 -> X2 -> X3                    |

Figura (histograma): `figures\sim1_Bellman_n10_hist.png`

Figura (série por vértice): `figures\sim1_Bellman_n10_series.png`

Figura (grafo):

![](figures\sim1_Bellman_n10_graph.png)

**Comentário:** em DAGs densos, um aumento de densidade tende a reduzir distâncias médias (mais opções de atalhos). Custos negativos podem criar caminhos muito curtos, mas como não há ciclos, não há risco de reduzir indefinidamente.

### Execução: n=100

- Arestas (m): 1307 | densidade efetiva: 0.132 | arestas negativas: 462

- Alcançáveis a partir de X1: 100/100 (inalcançáveis: 0)

- Tempo de execução: 0.000389 s

- Contadores internos: heap_pop=nan, heap_push=nan, iterations=nan, negative_cycle=nan, recursion_calls=1407.0, relax_checks=1307.0, relaxations=nan

- Hops (arestas no caminho): min=0 | média=18.12 | max=35 | desvio=9.57

- Indicador de espalhamento (dist_max / dist_mean): -0.40. Valores mais altos sugerem maior heterogeneidade entre caminhos curtos e longos.

#### Vértices mais distantes (top 10)

| label | distance | path                                   |
| ----- | -------- | -------------------------------------- |
| X8    | 50.0000  | X1 -> X2 -> X3 -> X4 -> X6 -> X7 -> X8 |
| X7    | 37.0000  | X1 -> X2 -> X3 -> X4 -> X6 -> X7       |
| X6    | 20.0000  | X1 -> X2 -> X3 -> X4 -> X6             |
| X5    | 18.0000  | X1 -> X2 -> X3 -> X4 -> X5             |
| X2    | 16.0000  | X1 -> X2                               |
| X10   | 11.0000  | X1 -> X2 -> X3 -> X9 -> X10            |
| X9    | 7.0000   | X1 -> X2 -> X3 -> X9                   |
| X4    | 5.0000   | X1 -> X2 -> X3 -> X4                   |
| X3    | 1.0000   | X1 -> X2 -> X3                         |
| X1    | 0.0000   | X1                                     |

#### Vértices mais próximos (top 10)

| label | distance  | path                                             |
| ----- | --------- | ------------------------------------------------ |
| X99   | -295.0000 | X1 -> X2 -> X3 -> X4 -> X15 -> X16 -> X17 -> X2… |
| X100  | -291.0000 | X1 -> X2 -> X3 -> X4 -> X15 -> X16 -> X17 -> X2… |
| X98   | -286.0000 | X1 -> X2 -> X3 -> X4 -> X15 -> X16 -> X17 -> X2… |
| X96   | -281.0000 | X1 -> X2 -> X3 -> X4 -> X15 -> X16 -> X17 -> X2… |
| X93   | -278.0000 | X1 -> X2 -> X3 -> X4 -> X15 -> X16 -> X17 -> X2… |
| X97   | -270.0000 | X1 -> X2 -> X3 -> X4 -> X15 -> X16 -> X17 -> X2… |
| X92   | -265.0000 | X1 -> X2 -> X3 -> X4 -> X15 -> X16 -> X17 -> X2… |
| X94   | -264.0000 | X1 -> X2 -> X3 -> X4 -> X15 -> X16 -> X17 -> X2… |
| X95   | -263.0000 | X1 -> X2 -> X3 -> X4 -> X15 -> X16 -> X17 -> X2… |
| X90   | -251.0000 | X1 -> X2 -> X3 -> X4 -> X15 -> X16 -> X17 -> X2… |

Figura (histograma): `figures\sim1_Bellman_n100_hist.png`

Figura (série por vértice): `figures\sim1_Bellman_n100_series.png`

Figura (grafo) indisponível: Visualização do grafo desativada para n >= 100

**Comentário:** em DAGs densos, um aumento de densidade tende a reduzir distâncias médias (mais opções de atalhos). Custos negativos podem criar caminhos muito curtos, mas como não há ciclos, não há risco de reduzir indefinidamente.

## Simulação 2 — Dijkstra Best-First com Heap (lista de sucessores, custos não-negativos)

**Ponto-chave:** o Dijkstra depende de pesos não-negativos. A fila de prioridade (Heap) garante que sempre expandimos o nó com menor distância conhecida (Best-First).

### Execução: n=10

- Arestas (m): 25 | densidade efetiva: 0.278 | arestas negativas: 0

- Alcançáveis a partir de X1: 10/10 (inalcançáveis: 0)

- Tempo de execução: 0.000022 s

- Contadores internos: heap_pop=10.0, heap_push=10.0, iterations=nan, negative_cycle=nan, recursion_calls=nan, relax_checks=nan, relaxations=9.0

- Hops (arestas no caminho): min=0 | média=2.10 | max=4 | desvio=1.14

- Indicador de espalhamento (dist_max / dist_mean): 2.21. Valores mais altos sugerem maior heterogeneidade entre caminhos curtos e longos.

#### Ranking de distância (mais perto → mais longe)

| label | distance | path                       |
| ----- | -------- | -------------------------- |
| X1    | 0.0000   | X1                         |
| X6    | 2.0000   | X1 -> X6                   |
| X9    | 3.0000   | X1 -> X6 -> X9             |
| X2    | 13.0000  | X1 -> X2                   |
| X4    | 25.0000  | X1 -> X6 -> X9 -> X4       |
| X7    | 27.0000  | X1 -> X6 -> X7             |
| X10   | 33.0000  | X1 -> X6 -> X9 -> X10      |
| X3    | 42.0000  | X1 -> X2 -> X3             |
| X5    | 42.0000  | X1 -> X6 -> X9 -> X4 -> X5 |
| X8    | 53.0000  | X1 -> X6 -> X7 -> X8       |

Figura (histograma): `figures\sim2_Dijkstra_n10_hist.png`

Figura (série por vértice): `figures\sim2_Dijkstra_n10_series.png`

Figura (grafo):

![](figures\sim2_Dijkstra_n10_graph.png)

**Comentário:** a forma Best-First com Heap prioriza nós com menor distância estimada. Em grafos mais densos, o número de relaxações cresce, mas a seleção ordenada mantém a correção.

### Execução: n=100

- Arestas (m): 2549 | densidade efetiva: 0.257 | arestas negativas: 0

- Alcançáveis a partir de X1: 100/100 (inalcançáveis: 0)

- Tempo de execução: 0.000261 s

- Contadores internos: heap_pop=254.0, heap_push=254.0, iterations=nan, negative_cycle=nan, recursion_calls=nan, relax_checks=nan, relaxations=253.0

- Hops (arestas no caminho): min=0 | média=3.38 | max=6 | desvio=1.43

- Indicador de espalhamento (dist_max / dist_mean): 1.79. Valores mais altos sugerem maior heterogeneidade entre caminhos curtos e longos.

#### Vértices mais distantes (top 10)

| label | distance | path                                         |
| ----- | -------- | -------------------------------------------- |
| X61   | 12.0000  | X1 -> X32 -> X38 -> X23 -> X59 -> X4 -> X61  |
| X37   | 11.0000  | X1 -> X76 -> X57 -> X36 -> X71 -> X6 -> X37  |
| X19   | 11.0000  | X1 -> X76 -> X57 -> X55 -> X19               |
| X40   | 11.0000  | X1 -> X32 -> X86 -> X14 -> X40               |
| X70   | 10.0000  | X1 -> X70                                    |
| X81   | 10.0000  | X1 -> X76 -> X57 -> X52 -> X68 -> X81        |
| X72   | 10.0000  | X1 -> X76 -> X57 -> X84 -> X34 -> X60 -> X72 |
| X100  | 10.0000  | X1 -> X32 -> X95 -> X100                     |
| X89   | 10.0000  | X1 -> X76 -> X57 -> X55 -> X85 -> X15 -> X89 |
| X62   | 10.0000  | X1 -> X27 -> X62                             |

#### Vértices mais próximos (top 10)

| label | distance | path                    |
| ----- | -------- | ----------------------- |
| X1    | 0.0000   | X1                      |
| X35   | 1.0000   | X1 -> X35               |
| X76   | 1.0000   | X1 -> X76               |
| X57   | 2.0000   | X1 -> X76 -> X57        |
| X90   | 2.0000   | X1 -> X35 -> X90        |
| X44   | 3.0000   | X1 -> X76 -> X57 -> X44 |
| X36   | 3.0000   | X1 -> X76 -> X57 -> X36 |
| X32   | 3.0000   | X1 -> X32               |
| X88   | 3.0000   | X1 -> X76 -> X88        |
| X83   | 3.0000   | X1 -> X83               |

Figura (histograma): `figures\sim2_Dijkstra_n100_hist.png`

Figura (série por vértice): `figures\sim2_Dijkstra_n100_series.png`

Figura (grafo) indisponível: Visualização do grafo desativada para n >= 100

**Comentário:** a forma Best-First com Heap prioriza nós com menor distância estimada. Em grafos mais densos, o número de relaxações cresce, mas a seleção ordenada mantém a correção.

## Simulação 3 — Floyd-Warshall (matriz de custos, custos negativos, ciclos)

**Ponto-chave:** o Floyd-Warshall calcula distâncias entre todos os pares, permitindo pesos negativos, e a resposta pedida (X1 -> demais) é a primeira linha da matriz final.

### Execução: n=10

- Arestas (m): 32 | densidade efetiva: 0.356 | arestas negativas: 9

- Alcançáveis a partir de X1: 10/10 (inalcançáveis: 0)

- Tempo de execução: 0.001395 s

- Contadores internos: heap_pop=nan, heap_push=nan, iterations=810.0, negative_cycle=False, recursion_calls=nan, relax_checks=nan, relaxations=109.0

- Hops (arestas no caminho): min=0 | média=1.90 | max=3 | desvio=0.94

- Indicador de espalhamento (dist_max / dist_mean): 2.03. Valores mais altos sugerem maior heterogeneidade entre caminhos curtos e longos.

#### Ranking de distância (mais perto → mais longe)

| label | distance | path                  |
| ----- | -------- | --------------------- |
| X1    | 0.0000   | X1                    |
| X2    | 12.0000  | X1 -> X2              |
| X5    | 15.0000  | X1 -> X2 -> X4 -> X5  |
| X8    | 17.0000  | X1 -> X2 -> X6 -> X8  |
| X6    | 21.0000  | X1 -> X2 -> X6        |
| X7    | 25.0000  | X1 -> X7              |
| X3    | 31.0000  | X1 -> X2 -> X3        |
| X4    | 36.0000  | X1 -> X2 -> X4        |
| X9    | 39.0000  | X1 -> X2 -> X9        |
| X10   | 50.0000  | X1 -> X2 -> X3 -> X10 |

Figura (histograma): `figures\sim3_Floyd_n10_hist.png`

Figura (série por vértice): `figures\sim3_Floyd_n10_series.png`

Figura (grafo):

![](figures\sim3_Floyd_n10_graph.png)

**Comentário:** o custo O(n^3) do Floyd-Warshall domina rapidamente em n=100. Mesmo assim, ele fornece todas as distâncias entre pares, o que é útil quando queremos responder muitas consultas de caminho mínimo após uma única execução.

### Execução: n=100

- Arestas (m): 2499 | densidade efetiva: 0.252 | arestas negativas: 564

- Alcançáveis a partir de X1: 100/100 (inalcançáveis: 0)

- Tempo de execução: 0.764173 s

- Contadores internos: heap_pop=nan, heap_push=nan, iterations=968600.0, negative_cycle=False, recursion_calls=nan, relax_checks=nan, relaxations=50325.0

- Hops (arestas no caminho): min=0 | média=3.06 | max=8 | desvio=1.38

- Indicador de espalhamento (dist_max / dist_mean): 25.97. Valores mais altos sugerem maior heterogeneidade entre caminhos curtos e longos.

#### Vértices mais distantes (top 10)

| label | distance | path                                  |
| ----- | -------- | ------------------------------------- |
| X41   | 20.0000  | X1 -> X12 -> X41                      |
| X46   | 19.0000  | X1 -> X47 -> X87 -> X83 -> X46        |
| X79   | 19.0000  | X1 -> X47 -> X87 -> X90 -> X79        |
| X25   | 18.0000  | X1 -> X47 -> X87 -> X90 -> X79 -> X25 |
| X5    | 18.0000  | X1 -> X29 -> X5                       |
| X50   | 18.0000  | X1 -> X58 -> X64 -> X37 -> X95 -> X50 |
| X93   | 17.0000  | X1 -> X93                             |
| X70   | 17.0000  | X1 -> X47 -> X87 -> X70               |
| X62   | 16.0000  | X1 -> X47 -> X72 -> X84 -> X62        |
| X74   | 16.0000  | X1 -> X12 -> X74                      |

#### Vértices mais próximos (top 10)

| label | distance | path                                             |
| ----- | -------- | ------------------------------------------------ |
| X3    | -20.0000 | X1 -> X47 -> X72 -> X60 -> X3                    |
| X29   | -20.0000 | X1 -> X29                                        |
| X52   | -19.0000 | X1 -> X47 -> X72 -> X84 -> X52                   |
| X60   | -18.0000 | X1 -> X47 -> X72 -> X60                          |
| X63   | -18.0000 | X1 -> X47 -> X72 -> X84 -> X88 -> X63            |
| X49   | -17.0000 | X1 -> X47 -> X15 -> X49                          |
| X17   | -15.0000 | X1 -> X47 -> X72 -> X84 -> X88 -> X89 -> X16 ->… |
| X9    | -15.0000 | X1 -> X29 -> X66 -> X9                           |
| X20   | -15.0000 | X1 -> X58 -> X20                                 |
| X24   | -14.0000 | X1 -> X47 -> X72 -> X84 -> X31 -> X24            |

Figura (histograma): `figures\sim3_Floyd_n100_hist.png`

Figura (série por vértice): `figures\sim3_Floyd_n100_series.png`

Figura (grafo) indisponível: Visualização do grafo desativada para n >= 100

**Comentário:** o custo O(n^3) do Floyd-Warshall domina rapidamente em n=100. Mesmo assim, ele fornece todas as distâncias entre pares, o que é útil quando queremos responder muitas consultas de caminho mínimo após uma única execução.

## Comparação entre algoritmos

| sim_id | sim_name | n   | runtime_s | eff_density | neg_edges | dist_mean | dist_std |
| ------ | -------- | --- | --------- | ----------- | --------- | --------- | -------- |
| 1      | Bellman  | 10  | 0.0000    | 0.2444      | 7         | -6.3000   | 33.5561  |
| 2      | Dijkstra | 10  | 0.0000    | 0.2778      | 0         | 24.0000   | 17.8941  |
| 3      | Floyd    | 10  | 0.0014    | 0.3556      | 9         | 24.6000   | 13.9657  |
| 1      | Bellman  | 100 | 0.0004    | 0.1320      | 462       | -126.2400 | 90.1513  |
| 2      | Dijkstra | 100 | 0.0003    | 0.2575      | 0         | 6.7000    | 2.4187   |
| 3      | Floyd    | 100 | 0.7642    | 0.2524      | 564       | 0.7700    | 11.3330  |

### Observações
- Em termos de complexidade assintótica, Dijkstra com Heap costuma escalar melhor para grafos esparsos a moderadamente densos, enquanto Floyd-Warshall cresce com n^3 e se torna o gargalo em tamanhos maiores.
- A simulação 1 é estruturalmente diferente: como é um DAG, o caminho mínimo pode ser resolvido via DP/topologia. A recursão com memoização tem custo proporcional a O(n+m).
- A presença de arestas negativas (sem ciclos negativos) pode deslocar a distribuição de distâncias para valores menores e aumentar o espalhamento.

## Parte 2 — Linguagem generativa (prompts)

O enunciado pede resolver os mesmos problemas com uma linguagem generativa, usando um prompt que solicite apenas: 'computar o caminho mínimo entre a raiz X1 e os demais vértices'.
No código, o módulo `fluxo_redes.llm_part2` gera prompts padronizados para cada representação, e inclui um modo de demonstração offline.

### Exemplos de prompt (modelos)

#### Simulação 1 (lista de antecessores)

```
Dado um grafo direcionado com vértices X1..Xn e a seguinte lista de antecessores (para cada Xi: lista de (Xj,custo Xj->Xi)),
calcule apenas o custo do caminho mínimo de X1 até todos os demais vértices.
Devolva uma lista de n valores d(X1)..d(Xn).
(sem explicações adicionais)

ENTRADA:
<cole aqui a lista de antecessores>
```

#### Simulação 2 (lista de sucessores)

```
Dado um grafo direcionado com vértices X1..Xn e a seguinte lista de sucessores (para cada Xi: lista de (Xj,custo Xi->Xj)),
calcule apenas o custo do caminho mínimo de X1 até todos os demais vértices.
Devolva uma lista de n valores d(X1)..d(Xn).
(sem explicações adicionais)

ENTRADA:
<cole aqui a lista de sucessores>
```

#### Simulação 3 (matriz de custos)

```
Dado um grafo direcionado com vértices X1..Xn e a seguinte matriz de custos C (C[i][j] = custo Xi->Xj; use INF quando não existir arco),
calcule apenas o custo do caminho mínimo de X1 até todos os demais vértices.
Devolva a primeira linha da matriz final de distâncias (d(X1->X1)..d(X1->Xn)).
(sem explicações adicionais)

ENTRADA:
<cole aqui a matriz>
```
