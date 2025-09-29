# Prática 1 - Grafos: Cenário 2

Este repositório contém a solução para o Cenário 2 da atividade "Prática 1 - Grafos".

## Cenário 2: Otimizando Caminho com Regeneração

O problema consiste em encontrar o caminho que minimiza a energia líquida gasta por um carro elétrico para ir de um ponto de origem a um destino. A malha viária é modelada como um grafo direcionado.

As arestas do grafo possuem pesos que podem ser:
* **Positivos**: Representam trechos de consumo de energia, como subidas ou arranques.
* **Negativos**: Representam trechos onde a frenagem regenerativa devolve energia à bateria.

O objetivo é encontrar o caminho mínimo partindo do vértice 0 até o vértice 6, e o somatório do custo (energia) desse caminho.

### Escolha do Algoritmo: Bellman-Ford

Para este cenário, foi utilizado o **Algoritmo de Bellman-Ford**. A principal razão para essa escolha é a presença de arestas com pesos negativos no grafo, uma característica que impede o uso de algoritmos como o de Dijkstra.

O Bellman-Ford é projetado para funcionar corretamente em grafos com pesos de aresta negativos e também é capaz de detectar ciclos de peso negativo, o que o torna a escolha adequada para este problema.

### Implementação

O código, presente no arquivo `Questao2.py`, implementa o algoritmo de Bellman-Ford para encontrar os caminhos mais curtos a partir de um único vértice de origem.

1.  **Leitura do Grafo**: O script lê o arquivo `graph2.txt` que contém a estrutura do grafo no formato:
    * Primeira linha: `<num_vertices> <num_arestas>`.
    * Linhas seguintes: `<vertice_inicial> <vertice_final> <custo>`.

2.  **Função `bellman_ford`**:
    * Inicializa as distâncias para todos os vértices como infinito, com exceção da origem (vértice 0), que começa com distância 0.
    * Relaxa todas as arestas do grafo `V-1` vezes (onde `V` é o número de vértices), atualizando as distâncias para encontrar os caminhos mais curtos.
    * Ao final, realiza uma passagem adicional para verificar a existência de ciclos de peso negativo.

3.  **Função `obter_caminho`**:
    * Utiliza o array de predecessores, gerado pelo `bellman_ford`, para reconstruir o caminho do vértice de origem até cada um dos outros vértices.

### Como Executar

1.  Certifique-se de que os arquivos `Questao2.py` e `graph2.txt` estejam no mesmo diretório.
2.  Execute o script Python a partir do terminal:
    ```bash
    python Questao2.py
    ```

### Resultados

Após a execução do script com o grafo fornecido em `graph2.txt`, a saída indica o caminho de menor custo da origem (0) para o destino (6).

* **Caminho Mínimo (0 -> 6)**: `0 -> 1 -> 5 -> 6`
* **Somatório do Custo do Caminho**: `6`
