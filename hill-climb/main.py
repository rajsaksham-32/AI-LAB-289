import random

def calculate_conflicts(state):
    conflicts = 0
    N = len(state)
    for i in range(N):
        for j in range(i + 1, N):
            if state[i] == state[j]:
                conflicts += 1
            if abs(state[i] - state[j]) == abs(i - j):
                conflicts += 1
    return conflicts

def get_neighbors(state):
    neighbors = []
    N = len(state)
    for col in range(N):
        for row in range(N):
            if state[col] != row:
                new_state = state.copy()
                new_state[col] = row
                neighbors.append(new_state)
    return neighbors

def print_board(state):
    N = len(state)
    board = [["." for _ in range(N)] for _ in range(N)]
    for col in range(N):
        board[state[col]][col] = "Q"
    for row in board:
        print(" ".join(row))
    print()

def hill_climbing_nqueens(N=4):
    current_state = [random.randint(0, N - 1) for _ in range(N)]
    current_cost = calculate_conflicts(current_state)
    print_board(current_state)

    while True:
        if current_cost == 0:
            return current_state
        neighbors = get_neighbors(current_state)
        best_neighbor = min(neighbors, key=calculate_conflicts)
        best_cost = calculate_conflicts(best_neighbor)
        if best_cost >= current_cost:
            return current_state
        else:
            current_state, current_cost = best_neighbor, best_cost
            print_board(current_state)

solution = hill_climbing_nqueens(4)
print("Final Solution:", solution)
print("Conflicts:", calculate_conflicts(solution))