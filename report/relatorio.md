# Relatório — Fluxo em Redes (Caminho Mínimo)

Gerado em 2026-01-17T14:52:41.499761Z

## Visão geral

O projeto implementa três simulações de caminho mínimo a partir da raiz X1, com diferentes hipóteses sobre ciclos e sinais dos custos, e com representações distintas de grafo.

### Resumo executivo dos resultados

 sim_id   n    m  neg_edges  runtime_s  dist_reachable  dist_min  dist_mean  dist_max
      1  10   22          7   0.000040              10     -48.0      -6.30      39.0
      1 100 1307        462   0.000316             100    -295.0    -126.24      50.0
      2  10   25          0   0.000024              10       0.0      24.00      53.0
      2 100 2549          0   0.000420             100       0.0       6.70      12.0
      3  10   32          9   0.001087              10       0.0      24.60      50.0
      3 100 2499        564   1.199227             100     -20.0       0.77      20.0

## Simulação 1 — Bellman recursivo em DAG com custos negativos (lista de antecessores)

**Ponto-chave:** como o grafo não possui circuitos, a recorrência de Bellman é bem definida e pode ser avaliada recursivamente. A memoização é essencial para evitar recomputações.

### Execução: n=10

- Arestas (m): 22 | densidade efetiva: 0.244 | arestas negativas: 7

- Alcançáveis a partir de X1: 10/10 (inalcançáveis: 0)

- Tempo de execução: 0.000040 s

- Contadores internos: heap_pop=nan, heap_push=nan, iterations=nan, negative_cycle=nan, recursion_calls=32.0, relax_checks=22.0, relaxations=nan

- Hops (arestas no caminho): min=0 | média=2.30 | max=5 | desvio=1.42

- Indicador de espalhamento (dist_max / dist_mean): -6.19. Valores mais altos sugerem maior heterogeneidade entre caminhos curtos e longos.

#### Vértices mais distantes (top 5)

label  distance                 path
   X3      39.0       X1 -> X2 -> X3
   X4      37.0 X1 -> X2 -> X3 -> X4
   X5      27.0       X1 -> X2 -> X5
   X2      20.0             X1 -> X2
   X1       0.0                   X1

#### Vértices mais próximos (top 5)

label  distance                              path
   X8     -48.0              X1 -> X6 -> X7 -> X8
  X10     -47.0 X1 -> X6 -> X7 -> X8 -> X9 -> X10
   X9     -44.0        X1 -> X6 -> X7 -> X8 -> X9
   X7     -30.0                    X1 -> X6 -> X7
   X6     -17.0                          X1 -> X6

Figura (histograma): `figures\sim1_n10_hist.png`

Figura (série por vértice): `figures\sim1_n10_series.png`

**Comentário:** em DAGs densos, um aumento de densidade tende a reduzir distâncias médias (mais opções de atalhos). Custos negativos podem criar caminhos muito curtos, mas como não há ciclos, não há risco de reduzir indefinidamente.

### Execução: n=100

- Arestas (m): 1307 | densidade efetiva: 0.132 | arestas negativas: 462

- Alcançáveis a partir de X1: 100/100 (inalcançáveis: 0)

- Tempo de execução: 0.000316 s

- Contadores internos: heap_pop=nan, heap_push=nan, iterations=nan, negative_cycle=nan, recursion_calls=1407.0, relax_checks=1307.0, relaxations=nan

- Hops (arestas no caminho): min=0 | média=18.12 | max=35 | desvio=9.57

- Indicador de espalhamento (dist_max / dist_mean): -0.40. Valores mais altos sugerem maior heterogeneidade entre caminhos curtos e longos.

#### Vértices mais distantes (top 5)

label  distance                                   path
   X8      50.0 X1 -> X2 -> X3 -> X4 -> X6 -> X7 -> X8
   X7      37.0       X1 -> X2 -> X3 -> X4 -> X6 -> X7
   X6      20.0             X1 -> X2 -> X3 -> X4 -> X6
   X5      18.0             X1 -> X2 -> X3 -> X4 -> X5
   X2      16.0                               X1 -> X2

#### Vértices mais próximos (top 5)

label  distance                                                                                                                                                                                                                                                 path
  X99    -295.0 X1 -> X2 -> X3 -> X4 -> X15 -> X16 -> X17 -> X20 -> X21 -> X25 -> X26 -> X33 -> X38 -> X39 -> X40 -> X41 -> X42 -> X43 -> X44 -> X61 -> X67 -> X68 -> X69 -> X70 -> X71 -> X77 -> X82 -> X83 -> X88 -> X89 -> X90 -> X91 -> X94 -> X95 -> X96 -> X99
 X100    -291.0       X1 -> X2 -> X3 -> X4 -> X15 -> X16 -> X17 -> X20 -> X21 -> X25 -> X26 -> X33 -> X38 -> X39 -> X40 -> X41 -> X42 -> X43 -> X44 -> X61 -> X67 -> X68 -> X69 -> X70 -> X71 -> X77 -> X82 -> X83 -> X88 -> X89 -> X90 -> X91 -> X92 -> X93 -> X100
  X98    -286.0        X1 -> X2 -> X3 -> X4 -> X15 -> X16 -> X17 -> X20 -> X21 -> X25 -> X26 -> X33 -> X38 -> X39 -> X40 -> X41 -> X42 -> X43 -> X44 -> X61 -> X67 -> X68 -> X69 -> X70 -> X71 -> X77 -> X82 -> X83 -> X88 -> X89 -> X90 -> X91 -> X94 -> X97 -> X98
  X96    -281.0        X1 -> X2 -> X3 -> X4 -> X15 -> X16 -> X17 -> X20 -> X21 -> X25 -> X26 -> X33 -> X38 -> X39 -> X40 -> X41 -> X42 -> X43 -> X44 -> X61 -> X67 -> X68 -> X69 -> X70 -> X71 -> X77 -> X82 -> X83 -> X88 -> X89 -> X90 -> X91 -> X94 -> X95 -> X96
  X93    -278.0               X1 -> X2 -> X3 -> X4 -> X15 -> X16 -> X17 -> X20 -> X21 -> X25 -> X26 -> X33 -> X38 -> X39 -> X40 -> X41 -> X42 -> X43 -> X44 -> X61 -> X67 -> X68 -> X69 -> X70 -> X71 -> X77 -> X82 -> X83 -> X88 -> X89 -> X90 -> X91 -> X92 -> X93

Figura (histograma): `figures\sim1_n100_hist.png`

Figura (série por vértice): `figures\sim1_n100_series.png`

**Comentário:** em DAGs densos, um aumento de densidade tende a reduzir distâncias médias (mais opções de atalhos). Custos negativos podem criar caminhos muito curtos, mas como não há ciclos, não há risco de reduzir indefinidamente.

## Simulação 2 — Dijkstra Best-First com Heap (lista de sucessores, custos não-negativos)

**Ponto-chave:** o Dijkstra depende de pesos não-negativos. A fila de prioridade (Heap) garante que sempre expandimos o nó com menor distância conhecida (Best-First).

### Execução: n=10

- Arestas (m): 25 | densidade efetiva: 0.278 | arestas negativas: 0

- Alcançáveis a partir de X1: 10/10 (inalcançáveis: 0)

- Tempo de execução: 0.000024 s

- Contadores internos: heap_pop=10.0, heap_push=10.0, iterations=nan, negative_cycle=nan, recursion_calls=nan, relax_checks=nan, relaxations=9.0

- Hops (arestas no caminho): min=0 | média=2.10 | max=4 | desvio=1.14

- Indicador de espalhamento (dist_max / dist_mean): 2.21. Valores mais altos sugerem maior heterogeneidade entre caminhos curtos e longos.

#### Vértices mais distantes (top 5)

label  distance                       path
   X8      53.0       X1 -> X6 -> X7 -> X8
   X3      42.0             X1 -> X2 -> X3
   X5      42.0 X1 -> X6 -> X9 -> X4 -> X5
  X10      33.0      X1 -> X6 -> X9 -> X10
   X7      27.0             X1 -> X6 -> X7

#### Vértices mais próximos (top 5)

label  distance                 path
   X1       0.0                   X1
   X6       2.0             X1 -> X6
   X9       3.0       X1 -> X6 -> X9
   X2      13.0             X1 -> X2
   X4      25.0 X1 -> X6 -> X9 -> X4

Figura (histograma): `figures\sim2_n10_hist.png`

Figura (série por vértice): `figures\sim2_n10_series.png`

**Comentário:** a forma Best-First com Heap prioriza nós com menor distância estimada. Em grafos mais densos, o número de relaxações cresce, mas a seleção ordenada mantém a correção.

### Execução: n=100

- Arestas (m): 2549 | densidade efetiva: 0.257 | arestas negativas: 0

- Alcançáveis a partir de X1: 100/100 (inalcançáveis: 0)

- Tempo de execução: 0.000420 s

- Contadores internos: heap_pop=254.0, heap_push=254.0, iterations=nan, negative_cycle=nan, recursion_calls=nan, relax_checks=nan, relaxations=253.0

- Hops (arestas no caminho): min=0 | média=3.38 | max=6 | desvio=1.43

- Indicador de espalhamento (dist_max / dist_mean): 1.79. Valores mais altos sugerem maior heterogeneidade entre caminhos curtos e longos.

#### Vértices mais distantes (top 5)

label  distance                                        path
  X61      12.0 X1 -> X32 -> X38 -> X23 -> X59 -> X4 -> X61
  X19      11.0              X1 -> X76 -> X57 -> X55 -> X19
  X37      11.0 X1 -> X76 -> X57 -> X36 -> X71 -> X6 -> X37
  X40      11.0              X1 -> X32 -> X86 -> X14 -> X40
  X70      10.0                                   X1 -> X70

#### Vértices mais próximos (top 5)

label  distance             path
   X1       0.0               X1
  X35       1.0        X1 -> X35
  X76       1.0        X1 -> X76
  X57       2.0 X1 -> X76 -> X57
  X90       2.0 X1 -> X35 -> X90

Figura (histograma): `figures\sim2_n100_hist.png`

Figura (série por vértice): `figures\sim2_n100_series.png`

**Comentário:** a forma Best-First com Heap prioriza nós com menor distância estimada. Em grafos mais densos, o número de relaxações cresce, mas a seleção ordenada mantém a correção.

## Simulação 3 — Floyd-Warshall (matriz de custos, custos negativos, ciclos)

**Ponto-chave:** o Floyd-Warshall calcula distâncias entre todos os pares, permitindo pesos negativos, e a resposta pedida (X1 -> demais) é a primeira linha da matriz final.

### Execução: n=10

- Arestas (m): 32 | densidade efetiva: 0.356 | arestas negativas: 9

- Alcançáveis a partir de X1: 10/10 (inalcançáveis: 0)

- Tempo de execução: 0.001087 s

- Contadores internos: heap_pop=nan, heap_push=nan, iterations=810.0, negative_cycle=False, recursion_calls=nan, relax_checks=nan, relaxations=109.0

- Hops (arestas no caminho): min=0 | média=1.90 | max=3 | desvio=0.94

- Indicador de espalhamento (dist_max / dist_mean): 2.03. Valores mais altos sugerem maior heterogeneidade entre caminhos curtos e longos.

#### Vértices mais distantes (top 5)

label  distance                  path
  X10      50.0 X1 -> X2 -> X3 -> X10
   X9      39.0        X1 -> X2 -> X9
   X4      36.0        X1 -> X2 -> X4
   X3      31.0        X1 -> X2 -> X3
   X7      25.0              X1 -> X7

#### Vértices mais próximos (top 5)

label  distance                 path
   X1       0.0                   X1
   X2      12.0             X1 -> X2
   X5      15.0 X1 -> X2 -> X4 -> X5
   X8      17.0 X1 -> X2 -> X6 -> X8
   X6      21.0       X1 -> X2 -> X6

Figura (histograma): `figures\sim3_n10_hist.png`

Figura (série por vértice): `figures\sim3_n10_series.png`

**Comentário:** o custo O(n^3) do Floyd-Warshall domina rapidamente em n=100. Mesmo assim, ele fornece todas as distâncias entre pares, o que é útil quando queremos responder muitas consultas de caminho mínimo após uma única execução.

### Execução: n=100

- Arestas (m): 2499 | densidade efetiva: 0.252 | arestas negativas: 564

- Alcançáveis a partir de X1: 100/100 (inalcançáveis: 0)

- Tempo de execução: 1.199227 s

- Contadores internos: heap_pop=nan, heap_push=nan, iterations=968600.0, negative_cycle=False, recursion_calls=nan, relax_checks=nan, relaxations=50325.0

- Hops (arestas no caminho): min=0 | média=3.06 | max=8 | desvio=1.38

- Indicador de espalhamento (dist_max / dist_mean): 25.97. Valores mais altos sugerem maior heterogeneidade entre caminhos curtos e longos.

#### Vértices mais distantes (top 5)

label  distance                                  path
  X41      20.0                      X1 -> X12 -> X41
  X46      19.0        X1 -> X47 -> X87 -> X83 -> X46
  X79      19.0        X1 -> X47 -> X87 -> X90 -> X79
  X25      18.0 X1 -> X47 -> X87 -> X90 -> X79 -> X25
  X50      18.0 X1 -> X58 -> X64 -> X37 -> X95 -> X50

#### Vértices mais próximos (top 5)

label  distance                                  path
   X3     -20.0         X1 -> X47 -> X72 -> X60 -> X3
  X29     -20.0                             X1 -> X29
  X52     -19.0        X1 -> X47 -> X72 -> X84 -> X52
  X60     -18.0               X1 -> X47 -> X72 -> X60
  X63     -18.0 X1 -> X47 -> X72 -> X84 -> X88 -> X63

Figura (histograma): `figures\sim3_n100_hist.png`

Figura (série por vértice): `figures\sim3_n100_series.png`

**Comentário:** o custo O(n^3) do Floyd-Warshall domina rapidamente em n=100. Mesmo assim, ele fornece todas as distâncias entre pares, o que é útil quando queremos responder muitas consultas de caminho mínimo após uma única execução.

## Comparação entre algoritmos

 sim_id   n  runtime_s  eff_density  neg_edges  dist_mean  dist_std
      1  10   0.000040     0.244444          7      -6.30 33.556072
      2  10   0.000024     0.277778          0      24.00 17.894133
      3  10   0.001087     0.355556          9      24.60 13.965672
      1 100   0.000316     0.132020        462    -126.24 90.151331
      2 100   0.000420     0.257475          0       6.70  2.418677
      3 100   1.199227     0.252424        564       0.77 11.333009

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
