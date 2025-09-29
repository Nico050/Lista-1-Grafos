import heapq                                                                    # Importa a biblioteca para implementação de fila de prioridade (min-heap).

class WarehouseRobot:                                                           # Definição da classe que encapsula toda a lógica do robô.
    def __init__(self, grid_file=None, grid_data=None):                          # Método construtor da classe.
   
        if grid_file:                                                            # Verifica se um caminho de arquivo foi fornecido.
            self.grid, self.rows, self.cols = self._load_grid_from_file(grid_file)  # Carrega o grid a partir do arquivo.
        elif grid_data:                                                          # Senão, verifica se os dados do grid foram fornecidos como string.
            self.grid, self.rows, self.cols = self._load_grid_from_string(grid_data)  # Carrega o grid a partir da string.
        else:                                                                    # Se nenhuma fonte de dados for fornecida.
            raise ValueError("É necessário fornecer grid_file ou grid_data")     # Lança um erro.
        
        self.start_pos = self._find_position('S')                                # Encontra e armazena a posição inicial 'S'.
        self.goal_pos = self._find_position('G')                                 # Encontra e armazena a posição do objetivo 'G'.
        
        # Custos para cada tipo de célula
        self.costs = {
            '.': 1,                                                              # Célula livre tem custo 1.
            '~': 3,                                                              # Piso difícil tem custo 3.
            'S': 1,                                                              # A célula inicial tem custo 1 para sair dela.
            'G': 1,                                                              # A célula objetivo tem custo 1 para entrar nela.
        }
        
        # Direções: Norte, Sul, Leste, Oeste
        self.directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    
    def _load_grid_from_file(self, filename):                                    # Método para carregar o grid de um arquivo.

        with open(filename, 'r') as f:                                           # Abre o arquivo no modo de leitura ('r').
            lines = f.read().strip().split('\n')                                 # Lê o conteúdo, remove espaços em branco extras e divide em linhas.
        
        rows, cols = map(int, lines[0].split())                                  # Lê a primeira linha para obter as dimensões.
        grid = []                                                                # Inicializa uma lista vazia para armazenar o grid.
        
        for i in range(1, rows + 1):                                             # Itera sobre as linhas de dados do grid.
            if i < len(lines):                                                   # Verifica se a linha existe no arquivo.
                line = lines[i].rstrip()                                         # Pega a linha e remove espaços em branco à direita.
                # Garante que a linha tenha o tamanho correto
                if len(line) < cols:                                             # Se a linha for mais curta que o esperado.
                    line += '.' * (cols - len(line))                             # Preenche o restante com células livres.
                elif len(line) > cols:                                           # Se a linha for mais longa que o esperado.
                    line = line[:cols]                                           # Trunca a linha para o tamanho correto.
                grid.append(list(line))                                          # Adiciona a linha processada ao grid.
            else:                                                                # Se o arquivo tiver menos linhas que o especificado.
                # Se não há linha suficiente, preenche com células livres
                grid.append(['.'] * cols)
        
        return grid, rows, cols                                                  # Retorna o grid, o número de linhas e colunas.
    
    def _load_grid_from_string(self, grid_data):                                 # Método para carregar o grid de uma string.

        lines = grid_data.strip().split('\n')                                    # Remove espaços extras da string e a divide em linhas.
        rows, cols = map(int, lines[0].split())                                  # Lê a primeira linha para as dimensões.
        grid = []                                                                # Inicializa a lista do grid.
        
        for i in range(1, rows + 1):                                             # Itera sobre as linhas de dados.
            if i < len(lines):                                                   # Se a linha existe.
                line = lines[i].rstrip()                                         # Remove espaços em branco à direita.
                # Garante que a linha tenha o tamanho correto
                if len(line) < cols:                                             # Se for curta.
                    line += '.' * (cols - len(line))                             # Preenche com células livres.
                elif len(line) > cols:                                           # Se for longa.
                    line = line[:cols]                                           # Trunca se for muito longa.
                grid.append(list(line))                                          # Adiciona ao grid.
            else:                                                                # Se faltarem linhas.
                # Se não há linha suficiente, preenche com células livres
                grid.append(['.'] * cols)
        
        return grid, rows, cols                                                  # Retorna os dados processados.
    
    def _find_position(self, char):                                              # Método para encontrar um caractere no grid.

        for i in range(self.rows):                                               # Itera sobre cada linha.
            for j in range(self.cols):                                           # Itera sobre cada coluna.
                if j < len(self.grid[i]) and self.grid[i][j] == char:            # Se a posição é válida e contém o caractere.
                    return (i, j)                                                # Retorna a tupla de coordenadas.
        raise ValueError(f"Caractere '{char}' não encontrado no grid")           # Lança um erro se o caractere não for encontrado.
    
    def _is_valid_position(self, row, col):                                      # Método para verificar se uma posição é válida.

        if 0 <= row < self.rows and 0 <= col < self.cols:                        # Verifica se as coordenadas estão dentro dos limites do grid.
            # Verifica se a linha existe e tem o índice da coluna
            if row < len(self.grid) and col < len(self.grid[row]):               # Checa se a célula existe na matriz de dados.
                return self.grid[row][col] != '#'                                # Retorna True se não for um obstáculo ('#').
            else:                                                                # Se a posição não existe no grid.
                # Se a posição não existe no grid, trata como célula livre
                return True
        return False                                                             # Retorna False se estiver fora dos limites.
    
    def _get_cost(self, row, col):                                               # Método para obter o custo de uma célula.

        if row < len(self.grid) and col < len(self.grid[row]):                   # Se a célula existe na matriz.
            cell = self.grid[row][col]                                           # Obtém o tipo de célula ('.', '~', etc.).
            return self.costs.get(cell, 1)                                       # Retorna o custo do dicionário. Usa 1 como padrão.
        else:                                                                    # Se a célula não existe.
            return 1                                                             # Retorna 1 (custo de célula livre) como padrão.
    
    def dijkstra(self):                                                          # Método principal que implementa o algoritmo de Dijkstra.
   
        # Heap para armazenar (custo, posição)
        heap = [(0, self.start_pos)]                                             # Inicia com a posição inicial e custo 0.
        
        # Dicionário para armazenar o menor custo para cada posição
        distances = {self.start_pos: 0}                                          # O custo para a posição inicial é 0.
        
        # Dicionário para reconstruir o caminho
        previous = {}
        
        visited = set()                                                          # Conjunto para guardar as posições já visitadas.
        
        while heap:                                                              # Loop principal: continua enquanto houver posições na fila.
            current_cost, current_pos = heapq.heappop(heap)                      # Pega a posição com o menor custo da fila.
            
            # Se chegamos ao objetivo
            if current_pos == self.goal_pos:                                     # Se a posição atual é o objetivo.
                path = self._reconstruct_path(previous, current_pos)             # Reconstrói o caminho.
                return path, current_cost                                        # Retorna o caminho e seu custo total.
            
            # Se já visitamos esta posição, pular
            if current_pos in visited:                                           # Se já visitamos e processamos esta posição.
                continue                                                         # Pula para a próxima iteração.
            
            visited.add(current_pos)                                             # Marca a posição atual como visitada.
            
            # Explorar vizinhos
            row, col = current_pos                                               # Desempacota as coordenadas da posição atual.
            for dr, dc in self.directions:                                       # Itera sobre as 4 direções de movimento.
                new_row, new_col = row + dr, col + dc                            # Calcula as coordenadas do vizinho.
                new_pos = (new_row, new_col)                                     # Cria a tupla da nova posição.
                
                if not self._is_valid_position(new_row, new_col):                # Se o vizinho é inválido.
                    continue                                                     # Pula para o próximo vizinho.
                
                if new_pos in visited:                                           # Se o vizinho já foi visitado.
                    continue                                                     # Pula para o próximo vizinho.
                
                # Calcular o novo custo
                move_cost = self._get_cost(new_row, new_col)                     # Pega o custo para entrar na célula do vizinho.
                new_cost = current_cost + move_cost                              # Soma ao custo acumulado até a posição atual.
                
                # Se encontramos um caminho mais barato
                if new_pos not in distances or new_cost < distances[new_pos]:
                    distances[new_pos] = new_cost                                # Atualiza o menor custo para o vizinho.
                    previous[new_pos] = current_pos                              # Registra que viemos de `current_pos`.
                    heapq.heappush(heap, (new_cost, new_pos))                    # Adiciona o vizinho à fila com seu novo custo.
        
        # Não foi possível encontrar um caminho
        return None, float('inf')                                                # Retorna None para o caminho e custo infinito.
    
    def _reconstruct_path(self, previous, goal_pos):                             # Método para reconstruir o caminho final.

        path = []                                                                # Inicializa a lista do caminho.
        current = goal_pos                                                       # Começa a partir do objetivo.
        
        while current is not None:                                               # Loop continua até chegar ao início.
            path.append(current)                                                 # Adiciona a posição atual ao caminho.
            current = previous.get(current)                                      # Move para a posição anterior no caminho.
        
        path.reverse()                                                           # Inverte a lista para ter a ordem do início ao fim.
        return path                                                              # Retorna o caminho completo.
    
    def print_grid_with_path(self, path=None):                                   # Método para imprimir o grid com o caminho.

        # Criar uma cópia do grid para não modificar o original
        display_grid = [row[:] for row in self.grid]                             # Cria uma cópia do grid para não modificar o original.
        
        if path:                                                                 # Se um caminho foi fornecido.
            for i, (row, col) in enumerate(path):                                # Itera sobre cada posição no caminho.
                if display_grid[row][col] not in ['S', 'G']:                     # Se a célula não for o início nem o fim.
                    display_grid[row][col] = '*'                                 # Marca a célula com um asterisco.
        
        for row in display_grid:                                                 # Itera sobre cada linha do grid de exibição.
            print(''.join(row))                                                  # Junta os caracteres da linha e a imprime no console.
    
    def solve(self):                                                             # Método principal que orquestra a solução e a exibição.
   
        print(f"Posição inicial (S): {self.start_pos}")                          # Imprime a posição inicial.
        print(f"Posição objetivo (G): {self.goal_pos}")                          # Imprime a posição objetivo.
        print()                                                                  # Imprime uma linha em branco para espaçamento.
        
        print(f"Grid original {self.rows}x{self.cols}:")                         # Título para o grid original.
        self.print_grid_with_path()                                              # Imprime o grid sem o caminho.
        print()                                                                  # Linha em branco.
        
        path, cost = self.dijkstra()                                             # Chama o algoritmo para encontrar o caminho e o custo.
        
        if path:                                                                 # Se um caminho foi encontrado.
            print("Caminho encontrado.")                                         # Mensagem de sucesso.
            print(f"Custo total: {cost}")                                        # Imprime o custo total do caminho.
            print(f"Número de passos: {len(path) - 1}")                          # Imprime o número de movimentos.
            print()                                                              # Linha em branco.
            
            print("Grid com caminho marcado (*):")                               # Título para o grid com o caminho.
            self.print_grid_with_path(path)                                      # Imprime o grid com o caminho marcado.
            print()                                                              # Linha em branco.
            
            print("Detalhes do caminho:")                                        # Título para os detalhes passo a passo.
            for i, (row, col) in enumerate(path):                                # Itera sobre cada passo do caminho.
                if row < len(self.grid) and col < len(self.grid[row]):           # Checa se a posição é válida.
                    cell_type = self.grid[row][col]                              # Obtém o tipo de célula do grid original.
                else:                                                            # Caso a posição seja válida mas não exista.
                    cell_type = '.'                                              # Assume como célula livre.
                
                if i == 0:                                                       # Se for o primeiro passo.
                    print(f"  Passo {i}: ({row},{col}) - Início (S)")             # Identifica como início.
                elif i == len(path) - 1:                                         # Se for o último passo.
                    print(f"  Passo {i}: ({row},{col}) - Objetivo (G)")           # Identifica como objetivo.
                else:                                                            # Para os passos intermediários.
                    if cell_type == '.':                                         # Se a célula for livre.
                        desc = "livre (custo 1)"
                    elif cell_type == '~':                                       # Se a célula for de piso difícil.
                        desc = "difícil (custo 3)"
                    else:                                                        # Para qualquer outro tipo de célula.
                        desc = f"tipo '{cell_type}' (custo 1)"
                    print(f"  Passo {i}: ({row},{col}) - {desc}")                 # Imprime os detalhes do passo.
        else:                                                                    # Se nenhum caminho foi encontrado.
            print("Não foi possível encontrar um caminho!")                      # Imprime a mensagem de falha.

# Exemplo de uso lendo arquivo
if __name__ == "__main__":                                                       # Bloco que executa apenas quando o script é rodado diretamente.
    robot = WarehouseRobot(grid_file="grid_example.txt")                         # Cria uma instância do robô, carregando o grid de um arquivo.
    robot.solve()                                                                # Chama o método `solve` para iniciar a busca e exibir os resultados.