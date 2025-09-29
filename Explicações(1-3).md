# Prática 1 - Grafos: Cenário 1
## Análise de Grafos: Estação Central com Floyd-Warshall

Este projeto implementa o algoritmo de Floyd-Warshall para encontrar os menores caminhos entre todos os pares de vértices em um grafo. O objetivo principal é identificar a "estação central", que é o vértice com a menor soma de distâncias para todos os outros vértices.

## Estrutura do Código

### 1. Importações e Variáveis Globais

```python
import numpy as np
import pprint

block_m = 1
block_md = 1
```
- **numpy**: Usado para manipulação eficiente de matrizes.
- **block_m e block_md**: Flags para controle de fluxo do programa, garantindo que as opções do menu sejam executadas na ordem correta.

### 2. Função `Matriz_Predecessor(matriz, matriz_p)`

**Propósito**: Inicializa a matriz de predecessores, que é essencial para a reconstrução dos caminhos mais curtos.

```python
def Matriz_Predecessor(matriz, matriz_p):
    for x in range(len(matriz)):
        for y in range(len(matriz)):
            if matriz[x,y] != np.inf:
                matriz_p[x,y] = x
```

### 3. Função `EncontrarEstacaoCentral(matriz)`

**Lógica**:
- Calcula a soma das distâncias de cada vértice para todos os outros (soma das linhas da matriz de distâncias).
- A estação central é o vértice com a menor soma total de distâncias.
- A função também identifica o vértice mais distante da estação central.

```python
def EncontrarEstacaoCentral(matriz):
    somas_distancias = np.sum(matriz, axis=1)
    indice_central = np.argmin(somas_distancias)
```

### 4. Função `Arquivo()`

**Funcionamento**:
- Lê um arquivo de grafo (`graph1.txt`) que deve estar no formato: `vértices arestas` na primeira linha, seguido por `origem destino peso` em cada linha subsequente.
- Cria uma matriz de adjacência onde `np.inf` representa a ausência de uma aresta direta.
- A diagonal principal da matriz é preenchida com zeros (distância de um vértice para ele mesmo).

```python
def Arquivo():
    caminho = 'c:/PROGRAMACAO/PROGRAMA.GRAFOS/graph1.txt'
    # Lê arquivo e constrói matriz de adjacência
```

### 5. Loop Principal - Menu Interativo

O programa principal opera através de um menu interativo com 5 opções:

1.  **Ler o grafo**:
    - Chama a função `Arquivo()` para carregar a matriz de adjacência do arquivo.
    - Atualiza `block_m = 0` para sinalizar que a matriz foi criada e outras opções podem ser executadas.

2.  **Criar matriz distância**:
    - Verifica se a matriz de adjacência já foi criada.
    - Inicializa `matriz_d` (cópia da matriz de adjacência) e `matriz_p` (matriz de predecessores).
    - Chama `Matriz_Predecessor()` para popular os predecessores iniciais.

3.  **Encontrar o melhor caminho (Floyd-Warshall)**:
    - Aplica o algoritmo de Floyd-Warshall para encontrar o menor caminho entre todos os pares de vértices.
    - Itera sobre todos os vértices `k` e atualiza a distância entre `i` e `j` se o caminho `i -> k -> j` for mais curto.
    - Atualiza a matriz de predecessores `matriz_p` sempre que um caminho menor é encontrado.
    ```python
    for k in range(len(matriz)):
        for i in range(len(matriz)):
            for j in range(len(matriz)):
                if matriz_d[i,j] > matriz_d[i,k] + matriz_d[k,j]:
                    matriz_d[i,j] = matriz_d[i,k] + matriz_d[k,j]
                    matriz_p[i,j] = matriz_d[k,j] # Nota: A atualização correta do predecessor geralmente usa matriz_p[k,j]
    ```

4.  **Mostrar resposta final**:
    - Chama `EncontrarEstacaoCentral()` usando a matriz de distâncias finais (`matriz_d`).
    - Exibe a estação central e o vértice mais distante dela.

5.  **Sair**:
    - Encerra a execução do programa.

## Conceitos de Teoria dos Grafos Aplicados

- **Algoritmo de Floyd-Warshall**: Um algoritmo de programação dinâmica para encontrar os caminhos mais curtos em um grafo direcionado com pesos, resolvendo o problema de todos os pares de caminhos mais curtos.



# Prática 1 - Grafos: Cenário 2

Este repositório contém a solução para o Cenário 2 da atividade "Prática 1 - Grafos".

## Cenário 2: Otimizando Caminho com Regeneração

O problema consiste em encontrar o caminho que minimiza a energia líquida gasta por um carro elétrico para ir de um ponto de origem a um destino. A malha viária é modelada como um grafo direcionado.

As arestas do grafo possuem pesos que podem ser:
* *Positivos*: Representam trechos de consumo de energia, como subidas ou arranques.
* *Negativos*: Representam trechos onde a frenagem regenerativa devolve energia à bateria.

O objetivo é encontrar o caminho mínimo partindo do vértice 0 até o vértice 6, e o somatório do custo (energia) desse caminho.

### Escolha do Algoritmo: Bellman-Ford

Para este cenário, foi utilizado o *Algoritmo de Bellman-Ford*. A principal razão para essa escolha é a presença de arestas com pesos negativos no grafo, uma característica que impede o uso de algoritmos como o de Dijkstra.

O Bellman-Ford é projetado para funcionar corretamente em grafos com pesos de aresta negativos e também é capaz de detectar ciclos de peso negativo, pois reexamina os caminhos para verificar se algum arco pode melhorá-los.

### Comparativo: Pseudocódigo vs. Implementação em Python

A seguir, uma comparação entre o pseudocódigo do algoritmo de Bellman-Ford apresentado na seção 3.2.2 do arquivo "algoritmos_caminho_minimo.pdf" e a implementação em Python no arquivo Questao2.py.

| Pseudocódigo (algoritmos_caminho_minimo.pdf) | Implementação (Questao2.py) | Análise |
| :--- | :--- | :--- |
| d11 ← 0; d1i ← ∞ ∀ i ∈ V-{1}; anterior (i) ← ∅;  | distancias = {i: float('Inf') for i in range(num_vertices)}<br>predecessores = {i: None for i in range(num_vertices)}<br>distancias[origem] = 0 | *Similaridade:* Ambas as abordagens iniciam as distâncias da origem como 0 e de todos os outros vértices como infinito. O vetor de predecessores (anterior) também é inicializado. |
| enquanto ∃(j,i) ∈ A | d1i > d1j + vji fazer`  | for _ in range(num_vertices - 1):<br>&nbsp;&nbsp;&nbsp;&nbsp;for u, v, peso in arestas: | *Diferença:* O pseudocódigo sugere um laço que continua enquanto houver melhorias nos caminhos. A implementação em Python adota a abordagem padrão e mais eficiente do Bellman-Ford, que consiste em relaxar todas as arestas V-1 vezes (onde V é o número de vértices). Isso garante a descoberta do caminho mínimo se não houver ciclos de peso negativo. |
| d1i ← d1j + vji; anterior (i) ← j  | if distancias[u] + peso < distancias[v]:<br>&nbsp;&nbsp;&nbsp;&nbsp;distancias[v] = distancias[u] + peso<br>&nbsp;&nbsp;&nbsp;&nbsp;predecessores[v] = u | *Similaridade:* A lógica central de "relaxamento" da aresta é idêntica. Se um caminho mais curto para um vértice v (ou i) é encontrado através de u (ou j), a distância e o predecessor são atualizados. |
| (Não explícito no pseudocódigo) | for u, v, peso in arestas:<br>&nbsp;&nbsp;&nbsp;&nbsp;if distancias[u] + peso < distancias[v]:<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;print("O grafo contém um ciclo de peso negativo") | *Diferença:* A implementação em Python inclui um laço extra após o principal para detectar explicitamente ciclos de peso negativo. Se for possível melhorar algum caminho após V-1 iterações, significa que um ciclo de peso negativo existe. O pseudocódigo não detalha essa verificação, embora sua condição enquanto implicitamente lidaria com isso (potencialmente entrando em um loop infinito). |

### Como Executar

1.  Certifique-se de que os arquivos Questao2.py e graph2.txt estejam no mesmo diretório.
2.  Execute o script Python a partir do terminal:
    bash
    python Questao2.py
    

### Resultados

Após a execução do script com o grafo fornecido em graph2.txt, a saída indica o caminho de menor custo da origem (0) para o destino (6).

* *Caminho Mínimo (0 -> 6)*: 0 -> 1 -> 5 -> 6
* *Somatório do Custo do Caminho*: 6




# Prática 1 - Grafos: Cenário 3
## Descrição do Problema

Um robô de inventário precisa navegar do ponto de recarga (S) até a docking station de coleta (G) dentro de um armazém. O ambiente possui:

O objetivo é encontrar o caminho que minimize o custo total, considerando os diferentes tipos de terreno e evitando obstáculos intransponíveis.

### Regras do Grid

O mapa é representado como um grid 2D com os seguintes elementos:

| Símbolo | Descrição | Custo |
|---------|-----------|-------|
| `.` | Célula livre (corredor normal) | 1 |
| `~` | Piso difícil (área com pallets) | 3 |
| `#` | Obstáculo (intransponível) | ∞ |
| `S` | Ponto de recarga (início) | 1 |
| `G` | Docking station (objetivo) | 1 |

**Movimentação**: O robô pode se mover em 4 direções (Norte, Sul, Leste, Oeste) - movimento diagonal não é permitido.

### Formato do Arquivo de Entrada

O arquivo `grid_example.txt` segue o formato:

10 15
```
~~####~~~~~~...
~~#..#.~~~~....
S.#..#..G......
..#..####~~....
..#.........~~.
..######..~~...
......#.~~##...
..##..#..###...
...............
```

## Escolha do Algoritmo: Dijkstra Otimizado

Para este cenário, foi utilizado o Algoritmo de Dijkstra. As principais razões para essa escolha:

### Por que Dijkstra?

1. **Pesos Não-Negativos**: Todos os custos de terreno são positivos (1 ou 3), permitindo o uso de Dijkstra
2. **Garantia de Otimalidade**: Encontra sempre o caminho de menor custo total
3. **Eficiência**: Com heap binária, complexidade O(E log V) é adequada para grids de tamanho moderado
4. **Custos Variáveis**: Suporta diferentes custos de terreno naturalmente

### Comparação com Algoritmo Clássico

| Aspecto | Dijkstra Clássico | Implementação Grid |
|---------|-------------------|-------------------|
| Estrutura de Dados | Arrays + busca linear | Heap + dicionários |
| Complexidade | O(V²) | O(E log V) |
| Representação | Grafo explícito | Grafo implícito |
| Exploração | Todos os vértices | Parada antecipada |
| Custos | Fixos nas arestas | Baseados em terreno |

### Comparação Detalhada: Pseudocódigo vs Implementação

#### 1. Inicialização

**Pseudocódigo Clássico:**
```
d₁₁ ← 0; d₁ⱼ ← ∞ ∀ i ∈ V - {1}
A ← V; F ← ∅; anterior(i) ← 0 ∀ i
```

**Nossa Implementação:**
```python
heap = [(0, self.start_pos)]
distances = {self.start_pos: 0}
previous = {}
visited = set()
```

**Diferenças:**

- **Heap** em vez de busca linear para melhor eficiência
- **Dicionário esparso** para distâncias (só armazena conhecidas, não inicializa tudo com ∞)
- **Coordenadas 2D** `(row, col)` em vez de índices simples
- **Set visited** equivalente ao conjunto F (fechado)



#### 2. Loop Principal

**Pseudocódigo Clássico:**
```
enquanto A ≠ ∅ fazer
    r ← v ∈ V | d₁ᵣ = min[d₁ⱼ]  // busca linear O(n)
    F ← F ∪ {r}; A ← A - {r}
```

**Nossa Implementação:**
```python
while heap:
    current_cost, current_pos = heapq.heappop(heap)
    if current_pos in visited:
        continue
    visited.add(current_pos)
```

**Diferenças:**

- heappop retorna automaticamente o vértice de menor distância em O(log n)
- Verificação de duplicatas para otimização
- Parada antecipada quando encontra objetivo (não processa todo o grafo)

#### 3. Relaxamento de Arestas

**Pseudocódigo Clássico:**
```
S ← A ∩ N⁺(r)
para todo i ∈ S fazer
    p ← min [d₁ᵢᵏ⁻¹, (d₁ᵣ + vᵣᵢ)]
    se p < d₁ᵢᵏ⁻¹ então
        d₁ᵢᵏ ← p; anterior(i) ← r
```

**Nossa Implementação:**
```python
for dr, dc in self.directions:
    new_row, new_col = row + dr, col + dc
    new_pos = (new_row, new_col)
    
    move_cost = self._get_cost(new_row, new_col)
    new_cost = current_cost + move_cost
    
    if new_pos not in distances or new_cost < distances[new_pos]:
        distances[new_pos] = new_cost
        previous[new_pos] = current_pos
        heapq.heappush(heap, (new_cost, new_pos))
```

**Diferenças:**

- **4-conectividade**: Explora apenas 4 direções (N, S, L, O)
- **Custo variável**: `move_cost` depende do tipo de célula (1 para '.', 3 para '~')
- **Validação explícita**: Verifica limites do grid e obstáculos
- **Heap dinâmica**: Adiciona novos caminhos ao heap conforme necessário

#### Resumo das Adaptações

A implementação mantém a essência do Dijkstra (sempre processar o vértice de menor distância e relaxar vizinhos), mas adapta:

1. **Estruturas de Dados**: Heap binária + dicionários para melhor performance
2. **Representação**: Grafo implícito específico para grid 2D
3. **Otimizações**: Parada antecipada e tratamento de duplicatas
4. **Domínio**: Custos baseados em tipo de terreno, não fixos nas arestas

## Implementação

O código está organizado na classe `WarehouseRobot`, que implementa:

### Principais Funcionalidades

1. **Carregamento de Grid**:
   - Suporte para leitura de arquivo ou string
   - Tratamento robusto de grids malformados
   - Normalização automática de dimensões

2. **Algoritmo de Dijkstra**:
   - Implementação otimizada com heap de prioridade
   - Validação de posições e obstáculos
   - Cálculo dinâmico de custos baseado em terreno

3. **Visualização de Resultados**:
   - Exibição do grid original
   - Grid com caminho marcado (usando asterisco)
   - Detalhamento passo-a-passo do percurso
 

### Estrutura do Código

A classe principal possui os seguintes métodos:

- `__init__()` - Inicializa robô e carrega grid
- `_load_grid_from_file()` - Carrega grid de arquivo
- `_load_grid_from_string()` - Carrega grid de string
- `_find_position()` - Localiza posições S e G
- `_is_valid_position()` - Valida se posição é transitável
- `_get_cost()` - Retorna custo do terreno
- `dijkstra()` - Executa algoritmo principal
- `_reconstruct_path()` - Reconstrói caminho ótimo
- `print_grid_with_path()` - Visualiza grid com caminho
- `save_grid_with_path_to_file()` - Salva resultado em arquivo
- `solve()` - Interface principal

### Fluxo de Execução

1. **Carregamento**: Lê e valida o grid do arquivo
2. **Localização**: Identifica posições S (origem) e G (destino)
3. **Execução**: Aplica algoritmo de Dijkstra
4. **Reconstrução**: Monta caminho ótimo usando predecessores
5. **Apresentação**: Exibe e salva resultados formatados

## Como Executar

### Pré-requisitos

- Bibliotecas padrão: `heapq`

### Passos para Execução

1. Certifique-se de que os arquivos `Questao3.py` e `grid_example.txt` estejam no mesmo diretório.

2. Execute o script Python:
   Apesar do arquivo estar em .py, foi testado apenas em .ipynb, por problemas ao importar o arquivo .ipynb não foi colocado no repositório, por isso recomendo copiar o código e testar em um notebook.

4. O programa irá:
   - Carregar o grid do arquivo
   - Encontrar o caminho ótimo
   - Exibir os resultados no terminal

### Exemplo de Uso em outra célula de código:

Você também pode usar o código assim::
```python

# Usando arquivo
robot = WarehouseRobot(grid_file="[insira o nome do seu mapa].txt")
robot.solve()

# Ou usando string diretamente
grid_data = """10 15
~~~~~~~~.......
~~####~~~~~~...
~~#..#.~~~~....
S.#..#..G......
..#..####~~....
..#.........~~.
..######..~~...
......#.~~##...
..##..#..###...
..............."""

robot = WarehouseRobot(grid_data=grid_data)
robot.solve()
```

## Resultados

Após a execução com o grid fornecido em `grid_example.txt`, o programa apresenta:

### Saída no Terminal
```
Posição inicial (S): (3, 0)
Posição objetivo (G): (3, 8)

Grid original 10x15:
~~~~~~~~.......
~~####~~~~~~...
~~#..#.~~~~....
S.#..#..G......
..#..####~~....
..#.........~~.
..######..~~...
......#.~~##...
..##..#..###...
...............

Caminho encontrado.
Custo total: 26
Número de passos: 22
Caminho: (3,0) -> (3,1) -> (4,1) -> ... -> (3,8)

Grid com caminho marcado (*):
~~~~~~~~.......
~~####~~~~~~...
~~#..#.~~~~....
S*#..#..G*.....
.*#..####*~....
.*#.....**..~~.
.*######*.~~...
.*****#**~##...
..##.*#*.###...
.....***.......

Detalhes do caminho:
  Passo 0: (3,0) - Início (S)
  Passo 1: (3,1) - livre (custo 1)
  ...
  Passo 22: (3,8) - Objetivo (G)
```

### Análise do Resultado

- **Caminho Completo**: `(3,0) -> (3,1) -> (4,1) -> (5,1) -> (6,1) -> (7,1) -> (7,2) -> (7,3) -> (7,4) -> (7,5) -> (8,5) -> (9,5) -> (9,6) -> (9,7) -> (8,7) -> (7,7) -> (7,8) -> (6,8) -> (5,8) -> (5,9) -> (4,9) -> (3,9) -> (3,8)`
- **Custo Total**: 26 unidades de energia
- **Número de Passos**: 22 movimentos

O algoritmo encontrou um caminho que:

- Evita todos os obstáculos (símbolo #)
- Minimiza o uso de pisos difíceis (símbolo ~)
- Prioriza corredores livres (símbolo .) sempre que possível
- Garante o menor custo total entre todas as rotas viáveis

**Autores**: Lucas, Nicolas, Matheus  
**Disciplina**: Teoria dos Grafos  
**Data**: 30/09/2025
```
