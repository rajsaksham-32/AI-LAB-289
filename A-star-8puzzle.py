from copy import deepcopy
import heapq

GOAL_STATE = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

DIRECTIONS = {
    'up': (-1, 0),
    'down': (1, 0),
    'left': (0, -1),
    'right': (0, 1)
}

def print_state(state):
    for row in state:
        print(row)
    print('-' * 10)

def state_to_tuple(state):
    return tuple(tuple(row) for row in state)

def find_zero(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

def move(state, direction):
    x, y = find_zero(state)
    dx, dy = DIRECTIONS[direction]
    nx, ny = x + dx, y + dy
    if 0 <= nx < 3 and 0 <= ny < 3:
        new_state = deepcopy(state)
        new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
        return new_state
    return None

# Manhattan Distance heuristic
def manhattan_distance(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            if value != 0:
                goal_x = (value - 1) // 3
                goal_y = (value - 1) % 3
                distance += abs(i - goal_x) + abs(j - goal_y)
    return distance

def a_star(start_state, goal_state):
    open_list = []
    g_score = {state_to_tuple(start_state): 0}
    f_score = {state_to_tuple(start_state): manhattan_distance(start_state)}
    heapq.heappush(open_list, (f_score[state_to_tuple(start_state)], start_state, []))

    visited = set()
    iteration = 0

    print("\nStarting A* Search...\n")

    while open_list:
        iteration += 1
        _, current_state, path = heapq.heappop(open_list)
        print(f"Iteration {iteration}:")
        print_state(current_state)
        print(f"g(n): {len(path)}, h(n): {manhattan_distance(current_state)}, f(n): {len(path) + manhattan_distance(current_state)}")

        state_key = state_to_tuple(current_state)
        if state_key in visited:
            continue
        visited.add(state_key)

        if current_state == goal_state:
            print("Goal state reached!\n")
            return path + [current_state]

        for direction in DIRECTIONS.keys():
            new_state = move(current_state, direction)
            if new_state:
                new_key = state_to_tuple(new_state)
                if new_key not in visited:
                    new_g = len(path) + 1
                    new_f = new_g + manhattan_distance(new_state)
                    heapq.heappush(open_list, (new_f, new_state, path + [current_state]))

    print("No solution found.")
    return None

if __name__ == "__main__":
    print("Enter the initial 3x3 puzzle state (use 0 for the blank):")
    initial_state = []
    for i in range(3):
        row = input(f"Row {i+1} (space-separated): ").strip().split()
        initial_state.append([int(num) for num in row])

    solution_path = a_star(initial_state, GOAL_STATE)

    if solution_path:
        print("Solution Path (step-by-step):")
        for idx, state in enumerate(solution_path):
            print(f"Step {idx}:")
            print_state(state)
        print(f"Puzzle Solved in {len(solution_path) - 1} moves!")
    else:
        print("Could not find a solution.")
