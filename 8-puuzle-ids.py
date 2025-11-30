N = 3
class PuzzleState:
    def __init__(self, board, x, y, depth):
        self.board = board
        self.x = x
        self.y = y
        self.depth = depth

row_moves = [0, 0, -1, 1]
col_moves = [-1, 1, 0, 0]
def is_goal_state(board):
    goal = [[1,2,3],[4,5,6],[7,0,8]]
    return board == goal
def is_valid(x, y):
    return 0 <= x < N and 0 <= y < N
def print_board(board):
    for r in board:
        print(' '.join(map(str, r)))
    print("--------")
def dfs_with_depth_limit(start, x, y, depth_limit):
    stack = []
    visited = set()
    stack.append(PuzzleState(start, x, y, 0))
    visited.add(tuple(map(tuple, start)))
    while stack:
        curr = stack.pop()
        print(f'Depth: {curr.depth}')
        print_board(curr.board)

        if is_goal_state(curr.board):
            print(f'Goal state reached at depth {curr.depth}')
            return True

        if curr.depth == depth_limit:
            continue

        for i in range(4):
            new_x = curr.x + row_moves[i]
            new_y = curr.y + col_moves[i]

            if is_valid(new_x, new_y):
                new_board = [row[:] for row in curr.board]
                new_board[curr.x][curr.y], new_board[new_x][new_y] = new_board[new_x][new_y], new_board[curr.x][curr.y]

                board_tuple = tuple(map(tuple, new_board))
                if board_tuple not in visited:
                    visited.add(board_tuple)
                    stack.append(PuzzleState(new_board, new_x, new_y, curr.depth + 1))
    return False
def iterative_deepening_search(start, x, y, max_depth=50):
    for depth in range(max_depth):
        print(f"Trying depth limit: {depth}")
        found = dfs_with_depth_limit(start, x, y, depth)
        if found:
            print(f"Solved at depth {depth}!")
            return
    print("No solution found within max depth limit.")
if __name__ == '__main__':
    start = [[1, 2, 3], [4, 0, 5], [6, 7, 8]]
    x, y = 1, 1
    print('Initial State:')
    print_board(start)
    iterative_deepening_search(start, x, y)
