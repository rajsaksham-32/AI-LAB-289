import numpy as np

# KB indices
S, B, P, W, V, G = 0, 1, 2, 3, 4, 5

# Wumpus World
class WumpusWorld:
    def __init__(self):
        self.world = np.matrix([    
            ['S', '', 'B', 'P'], 
            ['W', 'B,S,G', 'P', 'B'], 
            ['S', '', 'B', ''], 
            ['', 'B', 'P', 'B']
        ])

    def cell(self, col, row):
        content = self.world[4 - row, col - 1]
        return content.split(",") if content else []

# Agent
class Agent:
    def __init__(self, w_world, start_col=1, start_row=1):
        self.w_world = w_world
        self.c = start_col
        self.r = start_row
        self.kb = np.full((4,4,6), "", dtype=object)

    def loc(self): return np.array([self.c, self.r])

    def perceives(self):
        pos = self.loc()
        return self.w_world.cell(pos[0], pos[1])

    def adjacent(self):
        rows, cols = 4,4
        locs = []
        for r in [self.r-1, self.r+1]:
            if 0<r<=rows: locs.append((r,self.c))
        for c in [self.c-1, self.c+1]:
            if 0<c<=cols: locs.append((self.r,c))
        return locs

    def learn_from_pos(self):
        perc = self.perceives()
        kb_r, kb_c = 4 - self.r, self.c - 1
        # Current cell
        self.kb[kb_r,kb_c][V] = "V"
        self.kb[kb_r,kb_c][S] = "S" if "S" in perc else "~S"
        self.kb[kb_r,kb_c][B] = "B" if "B" in perc else "~B"
        self.kb[kb_r,kb_c][G] = "G" if "G" in perc else "~G"
        self.kb[kb_r,kb_c][P] = "~P"
        self.kb[kb_r,kb_c][W] = "~W"
        # Adjacent cells
        is_s = "S" in perc
        is_b = "B" in perc
        for (nr,nc) in self.adjacent():
            adj_r, adj_c = 4 - nr, nc -1
            self.kb[adj_r,adj_c][W] = "W?" if is_s and self.kb[adj_r,adj_c][W]=="" else "~W" if not is_s else self.kb[adj_r,adj_c][W]
            self.kb[adj_r,adj_c][P] = "P?" if is_b and self.kb[adj_r,adj_c][P]=="" else "~P" if not is_b else self.kb[adj_r,adj_c][P]

    def print_board(self):
        print("\nKB Board View:")
        for r in range(4):
            row = ""
            for c in range(4):
                cell = self.kb[r,c]
                # Display key info: Visited / Pit / Wumpus
                display = []
                if cell[V]=="V": display.append("V")
                if cell[P] != "": display.append(cell[P])
                if cell[W] != "": display.append(cell[W])
                row += f"{'/'.join(display):^10}"
            print(row)
        print()

def check_query(agent, qtype,row,col):
    kb_r,kb_c = 4-row, col-1
    val = agent.kb[kb_r,kb_c][P] if qtype=="Pit" else agent.kb[kb_r,kb_c][W]
    if val=="P" or val=="W": return True
    elif val=="~P" or val=="~W": return False
    elif val=="P?" or val=="W?": return "Possible"
    return None

# ---------------- Main ----------------
world = WumpusWorld()
agent = Agent(world)

agent.learn_from_pos()
agent.print_board()

# Queries
q1 = check_query(agent,"Pit",1,2)
q2 = check_query(agent,"Wumpus",2,2)

print(f"Query1: Is there a Pit at (1,2)? -> {q1}")
print(f"Query2: Is there a Wumpus at (2,2)? -> {q2}")
