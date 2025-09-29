import numpy as np
import pprint
block_m = 1
block_md = 1

def Matriz_Predecessor(matriz,matriz_p):
    for x in range(len(matriz)):
        for y in range(len(matriz)):

            if matriz[x,y] != np.inf:
                matriz_p[x,y] = x

def EncontrarEstacaoCentral(matriz):
   
    if matriz.size == 0:
        print('A matriz final ainda não foi calculada. Execute a opção 3 primeiro.')
        return

    somas_distancias = np.sum(matriz, axis=1)
    indice_central = np.argmin(somas_distancias)
    

    linha_matriz_central = list()
    for i in range(len(matriz)):
        linha_matriz_central.append (matriz[indice_central+1,i])
        
    mais_distante = np.argmax(linha_matriz_central)

    print(f'\nA Estação Central é a de número: {indice_central + 1}')
    print(matriz[indice_central])
    print(f'O vértice mais distante da estação central:{mais_distante} -----> Distancia:{matriz[indice_central,mais_distante]}\n')
    print(matriz)
    print('\n')

def Arquivo():
    try:
        # Mudar o caminho atravez dessa variavel #
        caminho = 'c:/PROGRAMACAO/PROGRAMA.GRAFOS/graph1.txt'
        with open(caminho, 'r', encoding='utf-8') as arquivo:
            lista_de_linhas = arquivo.readlines()
            for linha in lista_de_linhas:

                string_dos_numeros = linha.split(':')[0]

                strings_numericas = string_dos_numeros.strip().split()

                numeros = [int(s) for s in strings_numericas]


                if len(numeros) == 2:
                    num_vertices, num_arestas = numeros
                    matriz = np.full((num_vertices, num_vertices), np.inf)
                    for i in range(len(matriz)):
                        matriz[i,i] = 0

                elif len(numeros) == 3:
                    origem, destino, peso = numeros
                    matriz[origem-1][destino-1] = peso
                    matriz[destino-1][origem-1] = peso


    except FileNotFoundError:
        print("Erro: O arquivo não foi encontrado.")
    return matriz

while True:
    escolha=input('opcao 1:Ler o grafo\nopcao 2:Criar matriz distancia\nopcao 3:Encontrar o melhor caminho\nopcao 4:mostrar resposta final\nopcao 5:sair\n')

    if escolha == '1':

        block_m = 0
        matriz = Arquivo()
        print(matriz)
        print('\n')

    elif escolha == '2':

        if block_m == 1:
            print('crie primeiro a matriz\n')

        else:
            block_md = 0
            matriz_d = matriz
            matriz_p = np.full((12, 12), -1)
            print(matriz_d)
            print('\n')
            Matriz_Predecessor(matriz,matriz_p)
            print(matriz_p)
            print('\n')

    elif escolha == '3':
        if block_md == 0:
            for k in range(len(matriz)):
                for i in range(len(matriz)):
                    for j in range(len(matriz)):
                        if matriz_d[i,j] > matriz_d[i,k] + matriz_d[k,j]:
                            matriz_d[i,j] = matriz_d[i,k] + matriz_d[k,j]
                            matriz_p[i,j] = matriz_d[k,j]
        else:
            print('Crie primeiro a matriz distancia\n')

    elif escolha == '4':

        EncontrarEstacaoCentral(matriz_d)

    elif escolha == '5':

        break

    else:
        print('ERROU\n')
    