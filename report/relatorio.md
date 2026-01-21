# Relatório — Fluxo em Redes (Caminho Mínimo)

Gerado em 2026-01-21T00:02:41.778579Z

## Visão geral

O projeto implementa três simulações de caminho mínimo a partir da raiz X1, com diferentes hipóteses sobre ciclos e sinais dos custos, e com representações distintas de grafo.

## Simulação 1 — Bellman recursivo em DAG com custos negativos (lista de antecessores)

**Ponto-chave:** como o grafo não possui circuitos, a recorrência de Bellman é bem definida e pode ser avaliada recursivamente. A memoização é essencial para evitar recomputações.

### Execução: n=10

- Arestas (m): 22 | densidade efetiva: 0.244 | arestas negativas: 7

- Alcançáveis a partir de X1: 10/10 (inalcançáveis: 0)

- Tempo de execução: 0.000021 s

- Contadores internos: heap_pop=nan, heap_push=nan, iterations=nan, negative_cycle=nan, recursion_calls=32.0, relax_checks=22.0, relaxations=nan

- Hops (arestas no caminho): min=0 | média=2.30 | max=5 | desvio=1.42

- Indicador de espalhamento (dist_max / dist_mean): -6.19. Valores mais altos sugerem maior heterogeneidade entre caminhos curtos e longos.

Figura (grafo):

![](figures\sim1_Bellman_n10_graph.png)

#### Ranking de distância (mais perto → mais longe)

| label | distance | path                              |
| ----- | -------- | --------------------------------- |
| X8    | -48.00   | X1 -> X6 -> X7 -> X8              |
| X10   | -47.00   | X1 -> X6 -> X7 -> X8 -> X9 -> X10 |
| X9    | -44.00   | X1 -> X6 -> X7 -> X8 -> X9        |
| X7    | -30.00   | X1 -> X6 -> X7                    |
| X6    | -17.00   | X1 -> X6                          |
| X1    | 0.00     | X1                                |
| X2    | 20.00    | X1 -> X2                          |
| X5    | 27.00    | X1 -> X2 -> X5                    |
| X4    | 37.00    | X1 -> X2 -> X3 -> X4              |
| X3    | 39.00    | X1 -> X2 -> X3                    |

Figura (série por vértice): `figures\sim1_Bellman_n10_series.png`

**Comentário:** em DAGs densos, um aumento de densidade tende a reduzir distâncias médias (mais opções de atalhos). Custos negativos podem criar caminhos muito curtos, mas como não há ciclos, não há risco de reduzir indefinidamente.

### Execução: n=100

- Arestas (m): 1307 | densidade efetiva: 0.132 | arestas negativas: 462

- Alcançáveis a partir de X1: 100/100 (inalcançáveis: 0)

- Tempo de execução: 0.000424 s

- Contadores internos: heap_pop=nan, heap_push=nan, iterations=nan, negative_cycle=nan, recursion_calls=1407.0, relax_checks=1307.0, relaxations=nan

- Hops (arestas no caminho): min=0 | média=18.12 | max=35 | desvio=9.57

- Indicador de espalhamento (dist_max / dist_mean): -0.40. Valores mais altos sugerem maior heterogeneidade entre caminhos curtos e longos.

Figura (grafo) indisponível: Visualização do grafo desativada para n >= 100

#### Vértices mais distantes (top 10)

| label | distance | path                                   |
| ----- | -------- | -------------------------------------- |
| X8    | 50.00    | X1 -> X2 -> X3 -> X4 -> X6 -> X7 -> X8 |
| X7    | 37.00    | X1 -> X2 -> X3 -> X4 -> X6 -> X7       |
| X6    | 20.00    | X1 -> X2 -> X3 -> X4 -> X6             |
| X5    | 18.00    | X1 -> X2 -> X3 -> X4 -> X5             |
| X2    | 16.00    | X1 -> X2                               |
| X10   | 11.00    | X1 -> X2 -> X3 -> X9 -> X10            |
| X9    | 7.00     | X1 -> X2 -> X3 -> X9                   |
| X4    | 5.00     | X1 -> X2 -> X3 -> X4                   |
| X3    | 1.00     | X1 -> X2 -> X3                         |
| X1    | 0.00     | X1                                     |

#### Vértices mais próximos (top 10)

| label | distance | path                                             |
| ----- | -------- | ------------------------------------------------ |
| X99   | -295.00  | x1,x2,x3,x4,x15,x16,x17,x20,x21,x25,x26,x33,x38… |
| X100  | -291.00  | x1,x2,x3,x4,x15,x16,x17,x20,x21,x25,x26,x33,x38… |
| X98   | -286.00  | x1,x2,x3,x4,x15,x16,x17,x20,x21,x25,x26,x33,x38… |
| X96   | -281.00  | x1,x2,x3,x4,x15,x16,x17,x20,x21,x25,x26,x33,x38… |
| X93   | -278.00  | x1,x2,x3,x4,x15,x16,x17,x20,x21,x25,x26,x33,x38… |
| X97   | -270.00  | x1,x2,x3,x4,x15,x16,x17,x20,x21,x25,x26,x33,x38… |
| X92   | -265.00  | x1,x2,x3,x4,x15,x16,x17,x20,x21,x25,x26,x33,x38… |
| X94   | -264.00  | x1,x2,x3,x4,x15,x16,x17,x20,x21,x25,x26,x33,x38… |
| X95   | -263.00  | x1,x2,x3,x4,x15,x16,x17,x20,x21,x25,x26,x33,x38… |
| X90   | -251.00  | x1,x2,x3,x4,x15,x16,x17,x20,x21,x25,x26,x33,x38… |

Figura (série por vértice): `figures\sim1_Bellman_n100_series.png`

**Comentário:** em DAGs densos, um aumento de densidade tende a reduzir distâncias médias (mais opções de atalhos). Custos negativos podem criar caminhos muito curtos, mas como não há ciclos, não há risco de reduzir indefinidamente.

## Simulação 2 — Dijkstra Best-First com Heap (lista de sucessores, custos não-negativos)

**Ponto-chave:** o Dijkstra depende de pesos não-negativos. A fila de prioridade (Heap) garante que sempre expandimos o nó com menor distância conhecida (Best-First).

### Execução: n=10

- Arestas (m): 25 | densidade efetiva: 0.278 | arestas negativas: 0

- Alcançáveis a partir de X1: 10/10 (inalcançáveis: 0)

- Tempo de execução: 0.000039 s

- Contadores internos: heap_pop=10.0, heap_push=10.0, iterations=nan, negative_cycle=nan, recursion_calls=nan, relax_checks=nan, relaxations=9.0

- Hops (arestas no caminho): min=0 | média=2.10 | max=4 | desvio=1.14

- Indicador de espalhamento (dist_max / dist_mean): 2.21. Valores mais altos sugerem maior heterogeneidade entre caminhos curtos e longos.

Figura (grafo):

![](figures\sim2_Dijkstra_n10_graph.png)

#### Ranking de distância (mais perto → mais longe)

| label | distance | path                       |
| ----- | -------- | -------------------------- |
| X1    | 0.00     | X1                         |
| X6    | 2.00     | X1 -> X6                   |
| X9    | 3.00     | X1 -> X6 -> X9             |
| X2    | 13.00    | X1 -> X2                   |
| X4    | 25.00    | X1 -> X6 -> X9 -> X4       |
| X7    | 27.00    | X1 -> X6 -> X7             |
| X10   | 33.00    | X1 -> X6 -> X9 -> X10      |
| X3    | 42.00    | X1 -> X2 -> X3             |
| X5    | 42.00    | X1 -> X6 -> X9 -> X4 -> X5 |
| X8    | 53.00    | X1 -> X6 -> X7 -> X8       |

Figura (série por vértice): `figures\sim2_Dijkstra_n10_series.png`

**Comentário:** a forma Best-First com Heap prioriza nós com menor distância estimada. Em grafos mais densos, o número de relaxações cresce, mas a seleção ordenada mantém a correção.

### Execução: n=100

- Arestas (m): 2549 | densidade efetiva: 0.257 | arestas negativas: 0

- Alcançáveis a partir de X1: 100/100 (inalcançáveis: 0)

- Tempo de execução: 0.000386 s

- Contadores internos: heap_pop=254.0, heap_push=254.0, iterations=nan, negative_cycle=nan, recursion_calls=nan, relax_checks=nan, relaxations=253.0

- Hops (arestas no caminho): min=0 | média=3.38 | max=6 | desvio=1.43

- Indicador de espalhamento (dist_max / dist_mean): 1.79. Valores mais altos sugerem maior heterogeneidade entre caminhos curtos e longos.

Figura (grafo) indisponível: Visualização do grafo desativada para n >= 100

#### Vértices mais distantes (top 10)

| label | distance | path                                         |
| ----- | -------- | -------------------------------------------- |
| X61   | 12.00    | X1 -> X32 -> X38 -> X23 -> X59 -> X4 -> X61  |
| X37   | 11.00    | X1 -> X76 -> X57 -> X36 -> X71 -> X6 -> X37  |
| X19   | 11.00    | X1 -> X76 -> X57 -> X55 -> X19               |
| X40   | 11.00    | X1 -> X32 -> X86 -> X14 -> X40               |
| X70   | 10.00    | X1 -> X70                                    |
| X81   | 10.00    | X1 -> X76 -> X57 -> X52 -> X68 -> X81        |
| X72   | 10.00    | X1 -> X76 -> X57 -> X84 -> X34 -> X60 -> X72 |
| X100  | 10.00    | X1 -> X32 -> X95 -> X100                     |
| X89   | 10.00    | X1 -> X76 -> X57 -> X55 -> X85 -> X15 -> X89 |
| X62   | 10.00    | X1 -> X27 -> X62                             |

#### Vértices mais próximos (top 10)

| label | distance | path           |
| ----- | -------- | -------------- |
| X1    | 0.00     | x1             |
| X35   | 1.00     | x1,x35         |
| X76   | 1.00     | x1,x76         |
| X57   | 2.00     | x1,x76,x57     |
| X90   | 2.00     | x1,x35,x90     |
| X44   | 3.00     | x1,x76,x57,x44 |
| X36   | 3.00     | x1,x76,x57,x36 |
| X32   | 3.00     | x1,x32         |
| X88   | 3.00     | x1,x76,x88     |
| X83   | 3.00     | x1,x83         |

Figura (série por vértice): `figures\sim2_Dijkstra_n100_series.png`

**Comentário:** a forma Best-First com Heap prioriza nós com menor distância estimada. Em grafos mais densos, o número de relaxações cresce, mas a seleção ordenada mantém a correção.

## Simulação 3 — Floyd-Warshall (matriz de custos, custos negativos, ciclos)

**Ponto-chave:** o Floyd-Warshall calcula distâncias entre todos os pares, permitindo pesos negativos, e a resposta pedida (X1 -> demais) é a primeira linha da matriz final.

### Execução: n=10

- Arestas (m): 32 | densidade efetiva: 0.356 | arestas negativas: 9

- Alcançáveis a partir de X1: 10/10 (inalcançáveis: 0)

- Tempo de execução: 0.001228 s

- Contadores internos: heap_pop=nan, heap_push=nan, iterations=810.0, negative_cycle=False, recursion_calls=nan, relax_checks=nan, relaxations=109.0

- Hops (arestas no caminho): min=0 | média=1.90 | max=3 | desvio=0.94

- Indicador de espalhamento (dist_max / dist_mean): 2.03. Valores mais altos sugerem maior heterogeneidade entre caminhos curtos e longos.

Figura (grafo):

![](figures\sim3_Floyd_n10_graph.png)

#### Ranking de distância (mais perto → mais longe)

| label | distance | path                  |
| ----- | -------- | --------------------- |
| X1    | 0.00     | X1                    |
| X2    | 12.00    | X1 -> X2              |
| X5    | 15.00    | X1 -> X2 -> X4 -> X5  |
| X8    | 17.00    | X1 -> X2 -> X6 -> X8  |
| X6    | 21.00    | X1 -> X2 -> X6        |
| X7    | 25.00    | X1 -> X7              |
| X3    | 31.00    | X1 -> X2 -> X3        |
| X4    | 36.00    | X1 -> X2 -> X4        |
| X9    | 39.00    | X1 -> X2 -> X9        |
| X10   | 50.00    | X1 -> X2 -> X3 -> X10 |

Figura (série por vértice): `figures\sim3_Floyd_n10_series.png`

**Comentário:** o custo O(n^3) do Floyd-Warshall domina rapidamente em n=100. Mesmo assim, ele fornece todas as distâncias entre pares, o que é útil quando queremos responder muitas consultas de caminho mínimo após uma única execução.

### Execução: n=100

- Arestas (m): 2499 | densidade efetiva: 0.252 | arestas negativas: 564

- Alcançáveis a partir de X1: 100/100 (inalcançáveis: 0)

- Tempo de execução: 1.296992 s

- Contadores internos: heap_pop=nan, heap_push=nan, iterations=968600.0, negative_cycle=False, recursion_calls=nan, relax_checks=nan, relaxations=50325.0

- Hops (arestas no caminho): min=0 | média=3.06 | max=8 | desvio=1.38

- Indicador de espalhamento (dist_max / dist_mean): 25.97. Valores mais altos sugerem maior heterogeneidade entre caminhos curtos e longos.

Figura (grafo) indisponível: Visualização do grafo desativada para n >= 100

#### Vértices mais distantes (top 10)

| label | distance | path                                  |
| ----- | -------- | ------------------------------------- |
| X41   | 20.00    | X1 -> X12 -> X41                      |
| X46   | 19.00    | X1 -> X47 -> X87 -> X83 -> X46        |
| X79   | 19.00    | X1 -> X47 -> X87 -> X90 -> X79        |
| X25   | 18.00    | X1 -> X47 -> X87 -> X90 -> X79 -> X25 |
| X5    | 18.00    | X1 -> X29 -> X5                       |
| X50   | 18.00    | X1 -> X58 -> X64 -> X37 -> X95 -> X50 |
| X93   | 17.00    | X1 -> X93                             |
| X70   | 17.00    | X1 -> X47 -> X87 -> X70               |
| X62   | 16.00    | X1 -> X47 -> X72 -> X84 -> X62        |
| X74   | 16.00    | X1 -> X12 -> X74                      |

#### Vértices mais próximos (top 10)

| label | distance | path                               |
| ----- | -------- | ---------------------------------- |
| X3    | -20.00   | x1,x47,x72,x60,x3                  |
| X29   | -20.00   | x1,x29                             |
| X52   | -19.00   | x1,x47,x72,x84,x52                 |
| X60   | -18.00   | x1,x47,x72,x60                     |
| X63   | -18.00   | x1,x47,x72,x84,x88,x63             |
| X49   | -17.00   | x1,x47,x15,x49                     |
| X17   | -15.00   | x1,x47,x72,x84,x88,x89,x16,x55,x17 |
| X9    | -15.00   | x1,x29,x66,x9                      |
| X20   | -15.00   | x1,x58,x20                         |
| X24   | -14.00   | x1,x47,x72,x84,x31,x24             |

Figura (série por vértice): `figures\sim3_Floyd_n100_series.png`

**Comentário:** o custo O(n^3) do Floyd-Warshall domina rapidamente em n=100. Mesmo assim, ele fornece todas as distâncias entre pares, o que é útil quando queremos responder muitas consultas de caminho mínimo após uma única execução.

## Comparação entre algoritmos

| sim_id | sim_name | n   | runtime_s | eff_density | neg_edges | dist_mean | dist_std |
| ------ | -------- | --- | --------- | ----------- | --------- | --------- | -------- |
| 1      | Bellman  | 10  | 0.000021  | 0.24        | 7         | -6.30     | 33.56    |
| 2      | Dijkstra | 10  | 0.000039  | 0.28        | 0         | 24.00     | 17.89    |
| 3      | Floyd    | 10  | 0.001228  | 0.36        | 9         | 24.60     | 13.97    |
| 1      | Bellman  | 100 | 0.000424  | 0.13        | 462       | -126.24   | 90.15    |
| 2      | Dijkstra | 100 | 0.000386  | 0.26        | 0         | 6.70      | 2.42     |
| 3      | Floyd    | 100 | 1.296992  | 0.25        | 564       | 0.77      | 11.33    |

### Observações
- Em termos de complexidade assintótica, Dijkstra com Heap costuma escalar melhor para grafos esparsos a moderadamente densos, enquanto Floyd-Warshall cresce com n^3 e se torna o gargalo em tamanhos maiores.
- A simulação 1 é estruturalmente diferente: como é um DAG, o caminho mínimo pode ser resolvido via DP/topologia. A recursão com memoização tem custo proporcional a O(n+m).
- A presença de arestas negativas (sem ciclos negativos) pode deslocar a distribuição de distâncias para valores menores e aumentar o espalhamento.

## Resumo executivo dos resultados

| sim_id | sim_name | n   | m    | neg_edges | runtime_s | dist_reachable | dist_min | dist_mean | dist_max |
| ------ | -------- | --- | ---- | --------- | --------- | -------------- | -------- | --------- | -------- |
| 1      | Bellman  | 10  | 22   | 7         | 0.000021  | 10             | -48.00   | -6.30     | 39.00    |
| 1      | Bellman  | 100 | 1307 | 462       | 0.000424  | 100            | -295.00  | -126.24   | 50.00    |
| 2      | Dijkstra | 10  | 25   | 0         | 0.000039  | 10             | 0.00     | 24.00     | 53.00    |
| 2      | Dijkstra | 100 | 2549 | 0         | 0.000386  | 100            | 0.00     | 6.70      | 12.00    |
| 3      | Floyd    | 10  | 32   | 9         | 0.001228  | 10             | 0.00     | 24.60     | 50.00    |
| 3      | Floyd    | 100 | 2499 | 564       | 1.296992  | 100            | -20.00   | 0.77      | 20.00    |

### Parte 2 — Modelo utilizado e especificações

(ESCREVA AQUI)
- Modelo utilizado: GPT
- Versão/fornecedor: 5.2 Thinking
- Prompt final utilizado: Dado os grafos direcionados com vértices X1..Xn: (6 arquivos .txt anexados) calcule apenas o custo do caminho mínimo de X1 até todos os demais vértices Para cada um dos arquivos .txt anexados Devolva listas de n valores d(X1)..d(Xn), uma para cada arquivo .txt.
- Observações de execução: A LLM pensou por 2m e 37 segundos ao total para as 6 simulações


### Parte 2 — Comparação LLM vs algoritmos

| sim_id | sim_name | n   | n_alg | n_llm | matches | compared | mean_abs_diff | max_abs_diff |
| ------ | -------- | --- | ----- | ----- | ------- | -------- | ------------- | ------------ |
| 1      | Bellman  | 10  | 10    | 10    | 10      | 10       | 0.00          | 0.00         |
| 1      | Bellman  | 100 | 100   | 98    | 17      | 98       | 22.73         | 97.00        |
| 2      | Dijkstra | 10  | 10    | 10    | 10      | 10       | 0.00          | 0.00         |
| 2      | Dijkstra | 100 | 100   | 100   | 27      | 100      | 1.95          | 7.00         |
| 3      | Floyd    | 10  | 10    | 10    | 10      | 10       | 0.00          | 0.00         |
| 3      | Floyd    | 100 | 100   | 104   | 16      | 100      | 11.70         | 38.00        |

#### Lado a lado — sim1 Bellman n=10

| vertex | alg_distance | llm_distance | abs_diff |
| ------ | ------------ | ------------ | -------- |
| x1     | 0.00         | 0.00         | 0.00     |
| x2     | 20.00        | 20.00        | 0.00     |
| x3     | 39.00        | 39.00        | 0.00     |
| x4     | 37.00        | 37.00        | 0.00     |
| x5     | 27.00        | 27.00        | 0.00     |
| x6     | -17.00       | -17.00       | 0.00     |
| x7     | -30.00       | -30.00       | 0.00     |
| x8     | -48.00       | -48.00       | 0.00     |
| x9     | -44.00       | -44.00       | 0.00     |
| x10    | -47.00       | -47.00       | 0.00     |

#### Lado a lado — sim1 Bellman n=100

| vertex | alg_distance | llm_distance | abs_diff |
| ------ | ------------ | ------------ | -------- |
| x1     | 0.00         | 0.00         | 0.00     |
| x2     | 16.00        | 16.00        | 0.00     |
| x3     | 1.00         | 1.00         | 0.00     |
| x4     | 5.00         | 5.00         | 0.00     |
| x5     | 18.00        | 18.00        | 0.00     |
| x6     | 20.00        | 20.00        | 0.00     |
| x7     | 37.00        | 37.00        | 0.00     |
| x8     | 50.00        | 50.00        | 0.00     |
| x9     | 7.00         | 7.00         | 0.00     |
| x10    | 11.00        | 11.00        | 0.00     |
| x11    | -4.00        | -4.00        | 0.00     |
| x12    | -5.00        | -5.00        | 0.00     |
| x13    | 0.00         | 0.00         | 0.00     |
| x14    | -15.00       | -15.00       | 0.00     |
| x15    | -9.00        | -9.00        | 0.00     |
| x16    | -25.00       | -25.00       | 0.00     |
| x17    | -44.00       | -41.00       | 3.00     |
| x18    | -33.00       | -50.00       | 17.00    |
| x19    | -24.00       | -33.00       | 9.00     |
| x20    | -27.00       | -40.00       | 13.00    |
| x21    | -42.00       | -50.00       | 8.00     |
| x22    | -32.00       | -10.00       | 22.00    |
| x23    | -48.00       | -26.00       | 22.00    |
| x24    | -28.00       | -4.00        | 24.00    |
| x25    | -51.00       | -25.00       | 26.00    |
| x26    | -59.00       | -33.00       | 26.00    |
| x27    | -49.00       | -23.00       | 26.00    |
| x28    | -60.00       | -30.00       | 30.00    |
| x29    | -45.00       | -50.00       | 5.00     |
| x30    | -38.00       | -46.00       | 8.00     |
| x31    | -74.00       | -55.00       | 19.00    |
| x32    | -76.00       | -57.00       | 19.00    |
| x33    | -79.00       | -37.00       | 42.00    |
| x34    | -66.00       | -46.00       | 20.00    |
| x35    | -63.00       | -61.00       | 2.00     |
| x36    | -85.00       | -59.00       | 26.00    |
| x37    | -77.00       | -75.00       | 2.00     |
| x38    | -94.00       | -84.00       | 10.00    |
| x39    | -99.00       | -62.00       | 37.00    |
| x40    | -100.00      | -63.00       | 37.00    |
| x41    | -99.00       | -62.00       | 37.00    |
| x42    | -119.00      | -65.00       | 54.00    |
| x43    | -131.00      | -54.00       | 77.00    |
| x44    | -145.00      | -48.00       | 97.00    |
| x45    | -127.00      | -60.00       | 67.00    |
| x46    | -132.00      | -63.00       | 69.00    |
| x47    | -138.00      | -69.00       | 69.00    |
| x48    | -133.00      | -64.00       | 69.00    |
| x49    | -132.00      | -71.00       | 61.00    |
| x50    | -123.00      | -83.00       | 40.00    |
| x51    | -136.00      | -87.00       | 49.00    |
| x52    | -130.00      | -81.00       | 49.00    |
| x53    | -149.00      | -84.00       | 65.00    |
| x54    | -131.00      | -79.00       | 52.00    |
| x55    | -146.00      | -85.00       | 61.00    |
| x56    | -149.00      | -88.00       | 61.00    |
| x57    | -147.00      | -99.00       | 48.00    |
| x58    | -130.00      | -93.00       | 37.00    |
| x59    | -146.00      | -116.00      | 30.00    |
| x60    | -142.00      | -113.00      | 29.00    |
| x61    | -153.00      | -136.00      | 17.00    |
| x62    | -141.00      | -149.00      | 8.00     |
| x63    | -164.00      | -155.00      | 9.00     |
| x64    | -163.00      | -157.00      | 6.00     |
| x65    | -149.00      | -170.00      | 21.00    |
| x66    | -158.00      | -170.00      | 12.00    |
| x67    | -167.00      | -179.00      | 12.00    |
| x68    | -183.00      | -187.00      | 4.00     |
| x69    | -174.00      | -191.00      | 17.00    |
| x70    | -194.00      | -191.00      | 3.00     |
| x71    | -201.00      | -195.00      | 6.00     |
| x72    | -183.00      | -197.00      | 14.00    |
| x73    | -195.00      | -214.00      | 19.00    |
| x74    | -201.00      | -213.00      | 12.00    |
| x75    | -199.00      | -218.00      | 19.00    |
| x76    | -193.00      | -225.00      | 32.00    |
| x77    | -212.00      | -232.00      | 20.00    |
| x78    | -210.00      | -226.00      | 16.00    |
| x79    | -203.00      | -242.00      | 39.00    |
| x80    | -200.00      | -236.00      | 36.00    |
| x81    | -185.00      | -244.00      | 59.00    |
| x82    | -230.00      | -248.00      | 18.00    |
| x83    | -229.00      | -247.00      | 18.00    |
| x84    | -209.00      | -251.00      | 42.00    |
| x85    | -234.00      | -251.00      | 17.00    |
| x86    | -237.00      | -248.00      | 11.00    |
| x87    | -222.00      | -253.00      | 31.00    |
| x88    | -244.00      | -244.00      | 0.00     |
| x89    | -231.00      | -245.00      | 14.00    |
| x90    | -251.00      | -265.00      | 14.00    |
| x91    | -245.00      | -278.00      | 33.00    |
| x92    | -265.00      | -264.00      | 1.00     |
| x93    | -278.00      | -263.00      | 15.00    |
| x94    | -264.00      | -281.00      | 17.00    |
| x95    | -263.00      | -270.00      | 7.00     |
| x96    | -281.00      | -286.00      | 5.00     |
| x97    | -270.00      | -295.00      | 25.00    |
| x98    | -286.00      | -291.00      | 5.00     |

#### Lado a lado — sim2 Dijkstra n=10

| vertex | alg_distance | llm_distance | abs_diff |
| ------ | ------------ | ------------ | -------- |
| x1     | 0.00         | 0.00         | 0.00     |
| x2     | 13.00        | 13.00        | 0.00     |
| x3     | 42.00        | 42.00        | 0.00     |
| x4     | 25.00        | 25.00        | 0.00     |
| x5     | 42.00        | 42.00        | 0.00     |
| x6     | 2.00         | 2.00         | 0.00     |
| x7     | 27.00        | 27.00        | 0.00     |
| x8     | 53.00        | 53.00        | 0.00     |
| x9     | 3.00         | 3.00         | 0.00     |
| x10    | 33.00        | 33.00        | 0.00     |

#### Lado a lado — sim2 Dijkstra n=100

| vertex | alg_distance | llm_distance | abs_diff |
| ------ | ------------ | ------------ | -------- |
| x1     | 0.00         | 0.00         | 0.00     |
| x2     | 7.00         | 7.00         | 0.00     |
| x3     | 6.00         | 6.00         | 0.00     |
| x4     | 9.00         | 9.00         | 0.00     |
| x5     | 9.00         | 9.00         | 0.00     |
| x6     | 6.00         | 6.00         | 0.00     |
| x7     | 4.00         | 4.00         | 0.00     |
| x8     | 6.00         | 6.00         | 0.00     |
| x9     | 7.00         | 7.00         | 0.00     |
| x10    | 6.00         | 6.00         | 0.00     |
| x11    | 7.00         | 10.00        | 3.00     |
| x12    | 6.00         | 9.00         | 3.00     |
| x13    | 10.00        | 9.00         | 1.00     |
| x14    | 8.00         | 7.00         | 1.00     |
| x15    | 7.00         | 5.00         | 2.00     |
| x16    | 7.00         | 7.00         | 0.00     |
| x17    | 4.00         | 11.00        | 7.00     |
| x18    | 4.00         | 4.00         | 0.00     |
| x19    | 11.00        | 10.00        | 1.00     |
| x20    | 5.00         | 9.00         | 4.00     |
| x21    | 5.00         | 6.00         | 1.00     |
| x22    | 6.00         | 4.00         | 2.00     |
| x23    | 7.00         | 8.00         | 1.00     |
| x24    | 8.00         | 7.00         | 1.00     |
| x25    | 6.00         | 9.00         | 3.00     |
| x26    | 5.00         | 9.00         | 4.00     |
| x27    | 5.00         | 6.00         | 1.00     |
| x28    | 7.00         | 10.00        | 3.00     |
| x29    | 8.00         | 8.00         | 0.00     |
| x30    | 9.00         | 5.00         | 4.00     |
| x31    | 8.00         | 9.00         | 1.00     |
| x32    | 3.00         | 9.00         | 6.00     |
| x33    | 8.00         | 8.00         | 0.00     |
| x34    | 6.00         | 5.00         | 1.00     |
| x35    | 1.00         | 7.00         | 6.00     |
| x36    | 3.00         | 6.00         | 3.00     |
| x37    | 11.00        | 9.00         | 2.00     |
| x38    | 6.00         | 6.00         | 0.00     |
| x39    | 6.00         | 8.00         | 2.00     |
| x40    | 11.00        | 10.00        | 1.00     |
| x41    | 6.00         | 7.00         | 1.00     |
| x42    | 9.00         | 6.00         | 3.00     |
| x43    | 8.00         | 7.00         | 1.00     |
| x44    | 3.00         | 7.00         | 4.00     |
| x45    | 6.00         | 8.00         | 2.00     |
| x46    | 8.00         | 11.00        | 3.00     |
| x47    | 5.00         | 7.00         | 2.00     |
| x48    | 6.00         | 10.00        | 4.00     |
| x49    | 9.00         | 10.00        | 1.00     |
| x50    | 6.00         | 8.00         | 2.00     |
| x51    | 7.00         | 9.00         | 2.00     |
| x52    | 5.00         | 7.00         | 2.00     |
| x53    | 4.00         | 7.00         | 3.00     |
| x54    | 10.00        | 8.00         | 2.00     |
| x55    | 3.00         | 7.00         | 4.00     |
| x56    | 9.00         | 8.00         | 1.00     |
| x57    | 2.00         | 6.00         | 4.00     |
| x58    | 8.00         | 8.00         | 0.00     |
| x59    | 8.00         | 9.00         | 1.00     |
| x60    | 8.00         | 9.00         | 1.00     |
| x61    | 12.00        | 8.00         | 4.00     |
| x62    | 10.00        | 8.00         | 2.00     |
| x63    | 9.00         | 9.00         | 0.00     |
| x64    | 9.00         | 7.00         | 2.00     |
| x65    | 7.00         | 8.00         | 1.00     |
| x66    | 4.00         | 9.00         | 5.00     |
| x67    | 9.00         | 7.00         | 2.00     |
| x68    | 7.00         | 8.00         | 1.00     |
| x69    | 5.00         | 9.00         | 4.00     |
| x70    | 10.00        | 7.00         | 3.00     |
| x71    | 5.00         | 11.00        | 6.00     |
| x72    | 10.00        | 9.00         | 1.00     |
| x73    | 7.00         | 6.00         | 1.00     |
| x74    | 8.00         | 8.00         | 0.00     |
| x75    | 9.00         | 10.00        | 1.00     |
| x76    | 1.00         | 8.00         | 7.00     |
| x77    | 7.00         | 7.00         | 0.00     |
| x78    | 10.00        | 9.00         | 1.00     |
| x79    | 6.00         | 6.00         | 0.00     |
| x80    | 7.00         | 8.00         | 1.00     |
| x81    | 10.00        | 8.00         | 2.00     |
| x82    | 5.00         | 10.00        | 5.00     |
| x83    | 3.00         | 9.00         | 6.00     |
| x84    | 4.00         | 7.00         | 3.00     |
| x85    | 5.00         | 8.00         | 3.00     |
| x86    | 5.00         | 9.00         | 4.00     |
| x87    | 9.00         | 9.00         | 0.00     |
| x88    | 3.00         | 8.00         | 5.00     |
| x89    | 10.00        | 8.00         | 2.00     |
| x90    | 2.00         | 8.00         | 6.00     |
| x91    | 7.00         | 7.00         | 0.00     |
| x92    | 6.00         | 8.00         | 2.00     |
| x93    | 7.00         | 10.00        | 3.00     |
| x94    | 8.00         | 8.00         | 0.00     |
| x95    | 7.00         | 7.00         | 0.00     |
| x96    | 6.00         | 10.00        | 4.00     |
| x97    | 7.00         | 8.00         | 1.00     |
| x98    | 8.00         | 8.00         | 0.00     |
| x99    | 8.00         | 8.00         | 0.00     |
| x100   | 10.00        | 10.00        | 0.00     |

#### Lado a lado — sim3 Floyd n=10

| vertex | alg_distance | llm_distance | abs_diff |
| ------ | ------------ | ------------ | -------- |
| x1     | 0.00         | 0.00         | 0.00     |
| x2     | 12.00        | 12.00        | 0.00     |
| x3     | 31.00        | 31.00        | 0.00     |
| x4     | 36.00        | 36.00        | 0.00     |
| x5     | 15.00        | 15.00        | 0.00     |
| x6     | 21.00        | 21.00        | 0.00     |
| x7     | 25.00        | 25.00        | 0.00     |
| x8     | 17.00        | 17.00        | 0.00     |
| x9     | 39.00        | 39.00        | 0.00     |
| x10    | 50.00        | 50.00        | 0.00     |

#### Lado a lado — sim3 Floyd n=100

| vertex | alg_distance | llm_distance | abs_diff |
| ------ | ------------ | ------------ | -------- |
| x1     | 0.00         | 0.00         | 0.00     |
| x2     | -5.00        | -5.00        | 0.00     |
| x3     | -20.00       | -20.00       | 0.00     |
| x4     | -4.00        | -4.00        | 0.00     |
| x5     | 18.00        | 18.00        | 0.00     |
| x6     | -11.00       | -11.00       | 0.00     |
| x7     | 8.00         | 8.00         | 0.00     |
| x8     | -3.00        | -3.00        | 0.00     |
| x9     | -15.00       | -15.00       | 0.00     |
| x10    | 11.00        | 11.00        | 0.00     |
| x11    | -8.00        | -8.00        | 0.00     |
| x12    | 8.00         | 8.00         | 0.00     |
| x13    | 11.00        | 11.00        | 0.00     |
| x14    | 2.00         | 2.00         | 0.00     |
| x15    | -6.00        | -6.00        | 0.00     |
| x16    | 11.00        | -11.00       | 22.00    |
| x17    | -15.00       | -5.00        | 10.00    |
| x18    | 7.00         | 13.00        | 6.00     |
| x19    | 4.00         | -15.00       | 19.00    |
| x20    | -15.00       | 8.00         | 23.00    |
| x21    | -12.00       | -4.00        | 8.00     |
| x22    | -4.00        | -12.00       | 8.00     |
| x23    | 13.00        | 20.00        | 7.00     |
| x24    | -14.00       | -10.00       | 4.00     |
| x25    | 18.00        | 12.00        | 6.00     |
| x26    | 3.00         | -19.00       | 22.00    |
| x27    | -10.00       | 2.00         | 12.00    |
| x28    | 2.00         | 6.00         | 4.00     |
| x29    | -20.00       | -8.00        | 12.00    |
| x30    | -12.00       | 12.00        | 24.00    |
| x31    | 9.00         | 1.00         | 8.00     |
| x32    | -12.00       | -11.00       | 1.00     |
| x33    | 1.00         | -2.00        | 3.00     |
| x34    | 10.00        | -13.00       | 23.00    |
| x35    | -11.00       | 18.00        | 29.00    |
| x36    | 10.00        | -2.00        | 12.00    |
| x37    | 16.00        | -4.00        | 20.00    |
| x38    | -6.00        | 20.00        | 26.00    |
| x39    | 8.00         | -9.00        | 17.00    |
| x40    | -3.00        | 10.00        | 13.00    |
| x41    | 20.00        | 14.00        | 6.00     |
| x42    | -3.00        | 14.00        | 17.00    |
| x43    | 6.00         | -14.00       | 20.00    |
| x44    | -2.00        | 10.00        | 12.00    |
| x45    | 14.00        | -14.00       | 28.00    |
| x46    | 19.00        | 10.00        | 9.00     |
| x47    | -11.00       | -12.00       | 1.00     |
| x48    | -14.00       | 9.00         | 23.00    |
| x49    | -17.00       | 2.00         | 19.00    |
| x50    | 18.00        | 18.00        | 0.00     |
| x51    | 11.00        | 9.00         | 2.00     |
| x52    | -19.00       | 19.00        | 38.00    |
| x53    | -8.00        | 2.00         | 10.00    |
| x54    | 12.00        | 14.00        | 2.00     |
| x55    | 11.00        | 20.00        | 9.00     |
| x56    | 8.00         | 17.00        | 9.00     |
| x57    | -2.00        | -3.00        | 1.00     |
| x58    | -14.00       | -7.00        | 7.00     |
| x59    | -13.00       | -1.00        | 12.00    |
| x60    | -18.00       | 0.00         | 18.00    |
| x61    | -5.00        | 1.00         | 6.00     |
| x62    | 16.00        | 11.00        | 5.00     |
| x63    | -18.00       | 19.00        | 37.00    |
| x64    | -8.00        | 9.00         | 17.00    |
| x65    | 15.00        | -17.00       | 32.00    |
| x66    | 9.00         | 19.00        | 10.00    |
| x67    | -5.00        | 7.00         | 12.00    |
| x68    | -1.00        | 1.00         | 2.00     |
| x69    | -2.00        | -3.00        | 1.00     |
| x70    | 17.00        | -9.00        | 26.00    |
| x71    | 14.00        | -17.00       | 31.00    |
| x72    | -10.00       | 10.00        | 20.00    |
| x73    | -11.00       | 14.00        | 25.00    |
| x74    | 16.00        | 4.00         | 12.00    |
| x75    | -3.00        | 12.00        | 15.00    |
| x76    | 9.00         | -10.00       | 19.00    |
| x77    | -4.00        | 17.00        | 21.00    |
| x78    | 11.00        | -7.00        | 18.00    |
| x79    | 19.00        | 15.00        | 4.00     |
| x80    | -7.00        | -5.00        | 2.00     |
| x81    | -11.00       | -13.00       | 2.00     |
| x82    | 11.00        | -2.00        | 13.00    |
| x83    | 13.00        | -15.00       | 28.00    |
| x84    | -11.00       | 10.00        | 21.00    |
| x85    | 5.00         | -9.00        | 14.00    |
| x86    | 13.00        | -9.00        | 22.00    |
| x87    | -2.00        | 6.00         | 8.00     |
| x88    | 7.00         | 15.00        | 8.00     |
| x89    | -10.00       | -15.00       | 5.00     |
| x90    | 3.00         | 12.00        | 9.00     |
| x91    | 1.00         | -13.00       | 14.00    |
| x92    | -1.00        | 3.00         | 4.00     |
| x93    | 17.00        | 20.00        | 3.00     |
| x94    | 5.00         | 20.00        | 15.00    |
| x95    | 14.00        | 4.00         | 10.00    |
| x96    | -11.00       | -3.00        | 8.00     |
| x97    | -14.00       | 13.00        | 27.00    |
| x98    | 13.00        | -20.00       | 33.00    |
| x99    | 15.00        | -1.00        | 16.00    |
| x100   | 6.00         | -7.00        | 13.00    |
