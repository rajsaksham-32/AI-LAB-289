import random
import math

def random_state(n=8):
    """Generate a random board: list of row positions for each column."""
    return [random.randint(0, n - 1) for _ in range(n)]

def conflicts(state):
    """
    Number of attacking pairs of queens.
    Lower is better. A solution has 0.
    """
    h = 0
    n = len(state)

    for i in range(n):
        for j in range(i + 1, n):
   
            if state[i] == state[j]:
                h += 1
         
            if abs(state[i] - state[j]) == abs(i - j):
                h += 1
    return h

def random_neighbor(state):
    """
    Create a neighbor by moving a queen in one random column 
    to a random row.
    """
    n = len(state)
    new_state = state.copy()

    col = random.randint(0, n - 1)
    row = random.randint(0, n - 1)

    new_state[col] = row
    return new_state

def simulated_annealing(max_steps=100000, n=8):
 
    current = random_state(n)
    current_cost = conflicts(current)


    T = 1.0

    cooling = 0.0001

    for step in range(max_steps):

 
        if current_cost == 0:
            return current, step

        
        T = max(T * math.exp(-cooling * step), 0.0001)

       
        next_state = random_neighbor(current)
        next_cost = conflicts(next_state)

        
        delta = current_cost - next_cost

       
        if delta > 0 or random.random() < math.exp(delta / T):
            current = next_state
            current_cost = next_cost

    return None, max_steps


solution, steps = simulated_annealing()

if solution:
    print(f"Solution found in {steps} steps:")
    print("State:", solution)
    print("Conflicts:", conflicts(solution))
else:
    print("No solution found.")
