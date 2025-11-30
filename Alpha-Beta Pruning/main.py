import math

def alphabeta(node, depth, alpha, beta, maximizingPlayer):

    if depth == 0 or isinstance(node, int):
        return node

    if maximizingPlayer:
        value = -math.inf
        for child in node:
            value = max(value, alphabeta(child, depth - 1, alpha, beta, False))
            alpha = max(alpha, value)
            if beta <= alpha:
                print(f"Pruned in MAX node: alpha={alpha}, beta={beta}")
                break
        return value

    else:  
        value = math.inf
        for child in node:
            value = min(value, alphabeta(child, depth - 1, alpha, beta, True))
            beta = min(beta, value)
            if beta <= alpha:
                print(f"Pruned in MIN node: alpha={alpha}, beta={beta}")
                break
        return value



game_tree = [
    [3, 5, 6],      
    [1, 2, 4],      
    [7, 9, 8]       
]


result = alphabeta(game_tree, 2, -math.inf, math.inf, True)
print("\nFinal Result (Best value for Max):", result)
