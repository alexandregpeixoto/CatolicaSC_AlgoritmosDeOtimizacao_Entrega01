# Importa as classes necessárias para a implementação da busca
from queue import PriorityQueue
from itertools import count
import copy

# Define a classe para representar o estado do quebra-cabeça
class PuzzleState:
    def __init__(self, configuration):
        self.configuration = configuration

    def __str__(self):
        return str(self.configuration)

    def __eq__(self, other):
        return self.configuration == other.configuration

    def __hash__(self):
        return hash(str(self.configuration))

# Função que retorna as possíveis jogadas a partir de um estado
def get_possible_moves(state):
    moves = []
    for i in range(3):
        for j in range(3):
            if state.configuration[i][j] == 0:  # Encontra a posição da peça vazia
                if i > 0:
                    moves.append(swap_tiles(state, i, j, i - 1, j))
                if i < 2:
                    moves.append(swap_tiles(state, i, j, i + 1, j))
                if j > 0:
                    moves.append(swap_tiles(state, i, j, i, j - 1))
                if j < 2:
                    moves.append(swap_tiles(state, i, j, i, j + 1))
    return moves

# Função que troca as posições de duas peças e retorna um novo estado
def swap_tiles(state, i1, j1, i2, j2):
    new_config = copy.deepcopy(state.configuration)  # Evita modificar o estado original
    new_config[i1][j1], new_config[i2][j2] = new_config[i2][j2], new_config[i1][j1]
    return PuzzleState(new_config)

# Gera os sucessores de um estado
def generate_successors(state):
    return [PuzzleState(move.configuration) for move in get_possible_moves(state)]

# Calcula a distância de Manhattan entre dois estados do quebra-cabeça
def manhattan_distance(state, goal):
    distance = 0
    for i in range(3):
        for j in range(3):
            if state.configuration[i][j] != 0:
                goal_i, goal_j = find_position(goal.configuration, state.configuration[i][j])
                distance += abs(i - goal_i) + abs(j - goal_j)
    return max(0, distance)

# Encontra a posição de um valor em uma matriz
def find_position(matrix, value):
    for i in range(3):
        for j in range(3):
            if matrix[i][j] == value:
                return i, j

# Implementa a busca gulosa
def greedy_search(start, goal):
    explored = set()
    priority_queue = PriorityQueue()
    counter = count()

    priority_queue.put((0, next(counter), [start]))  # Começa com uma prioridade de 0

    while not priority_queue.empty():
        current_path = priority_queue.get()[2]
        current_state = current_path[-1]

        if current_state == goal:
            return current_path

        if current_state not in explored:
            explored.add(current_state)

            for successor in generate_successors(current_state):
                if successor not in explored:
                    new_path = list(current_path)
                    new_path.append(successor)
                    priority_queue.put((manhattan_distance(successor, goal), next(counter), new_path))

    return None

# Define as configurações inicial e final do quebra-cabeça
startValues = [
    [2, 8, 3],
    [1, 0, 6],
    [4, 7, 5]
]

endValues = [
    [1, 2, 3],
    [8, 0, 4],
    [7, 6, 5]
]

start_state = PuzzleState(startValues)
goal_state = PuzzleState(endValues)

# Executa a busca gulosa e imprime o caminho encontrado ou uma mensagem indicando que o caminho não foi encontrado
path = greedy_search(start_state, goal_state)

if path:
    print("Caminho encontrado:")
    for state in path:
        print(state)
else:
    print("Caminho não encontrado.")
