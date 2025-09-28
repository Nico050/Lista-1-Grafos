def bellman_ford(num_vertices, arestas, origem):

    distancias = {i: float('Inf') for i in range(num_vertices)}
    predecessores = {i: None for i in range(num_vertices)}
    distancias[origem] = 0

    for _ in range(num_vertices - 1):
        for u, v, peso in arestas:
            if distancias[u] != float('Inf') and distancias[u] + peso < distancias[v]:
                distancias[v] = distancias[u] + peso
                predecessores[v] = u

    for u, v, peso in arestas:
        if distancias[u] != float('Inf') and distancias[u] + peso < distancias[v]:
            print("O grafo contém um ciclo de peso negativo")
            return None, None

    return distancias, predecessores

def obter_caminho(predecessores, vertice_destino):

    caminho = []
    atual = vertice_destino
    while atual is not None:
        caminho.insert(0, str(atual))
        atual = predecessores[atual]
    return " -> ".join(caminho)


nome_arquivo = 'graph2.txt'
arestas_grafo = []

try:
    with open(nome_arquivo, 'r') as f:
        
        num_v, num_a = map(int, f.readline().split())

        for linha in f:
            u, v, peso = map(int, linha.split())
            arestas_grafo.append((u, v, peso))

    vertice_origem = 0

    dist, pred = bellman_ford(num_v, arestas_grafo, vertice_origem)

    if dist:
        print(f"Resultados do Algoritmo de Bellman-Ford (Origem: Vértice {vertice_origem})\n")
        print("{:<10} {:<15} {:<20}".format("Destino", "Custo Mínimo", "Caminho"))
        print("-" * 45)
        for i in range(num_v):
            caminho_str = obter_caminho(pred, i)
            print("{:<10} {:<15} {:<20}".format(i, dist[i], caminho_str))

except FileNotFoundError:
    print(f"Erro: O arquivo '{nome_arquivo}' não foi encontrado.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")