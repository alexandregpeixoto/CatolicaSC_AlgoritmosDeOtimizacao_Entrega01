from queue import PriorityQueue
from itertools import count
import copy

class PuzzleState:
    def __init__(self, configuration):
        self.configuration = configuration

    def __str__(self):
        return str(self.configuration)

    def __eq__(self, other):
        return self.configuration == other.configuration

    def __hash__(self):
        return hash(str(self.configuration))


def get_possible_moves(state):
    moves = []
    for i in range(3):
        for j in range(3):
            if state.configuration[i][j] == 0:  # Find the position of the empty tile
                if i > 0:
                    moves.append(swap_tiles(state, i, j, i - 1, j))
                if i < 2:
                    moves.append(swap_tiles(state, i, j, i + 1, j))
                if j > 0:
                    moves.append(swap_tiles(state, i, j, i, j - 1))
                if j < 2:
                    moves.append(swap_tiles(state, i, j, i, j + 1))

    return moves


def swap_tiles(state, i1, j1, i2, j2):
    new_config = copy.deepcopy(state.configuration)  # Avoid modifying the original state
    new_config[i1][j1], new_config[i2][j2] = new_config[i2][j2], new_config[i1][j1]
    return PuzzleState(new_config)


def generate_successors(state):
    return [PuzzleState(move.configuration) for move in get_possible_moves(state)]


def manhattan_distance(state, goal):
    distance = 0
    for i in range(3):
        for j in range(3):
            if state.configuration[i][j] != 0:
                goal_i, goal_j = find_position(goal.configuration, state.configuration[i][j])
                distance += abs(i - goal_i) + abs(j - goal_j)
    return max(0, distance)


def find_position(matrix, value):
    for i in range(3):
        for j in range(3):
            if matrix[i][j] == value:
                return i, j


def greedy_search(start, goal):
    explored = set()
    priority_queue = PriorityQueue()
    counter = count()

    priority_queue.put((0, next(counter), [start]))  # Start with a priority of 0

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

path = greedy_search(start_state, goal_state)

if path:
    print("Caminho encontrado:")
    for state in path:
        print(state)
else:
    print("Caminho não encontrado.")