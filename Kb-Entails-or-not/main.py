import itertools


class Formula:
    def __init__(self, symbols, expr):
        self.symbols = set(symbols)
        self.expr = expr  

    def evaluate(self, model):
        return self.expr(model)

def get_all_symbols(kb, query):
    symbols = set()
    for f in kb + [query]:
        symbols |= f.symbols
    return sorted(symbols)

def entails(kb, query):
    symbols = get_all_symbols(kb, query)

    for values in itertools.product([False, True], repeat=len(symbols)):
        model = dict(zip(symbols, values))

    
        if all(f.evaluate(model) for f in kb):
        
            if not query.evaluate(model):
                print("Counterexample found:", model)
                return False
    return True


R_implies_W = Formula({"R", "W"}, lambda m: (not m["R"]) or m["W"])


S_implies_W = Formula({"S", "W"}, lambda m: (not m["S"]) or m["W"])


W_implies_L = Formula({"W", "L"}, lambda m: (not m["W"]) or m["L"])

C_implies_R = Formula({"C", "R"}, lambda m: (not m["C"]) or m["R"])


S_or_C = Formula({"S", "C"}, lambda m: m["S"] or m["C"])


S_equiv_D = Formula({"S", "D"}, lambda m: m["S"] == m["D"])

Query_L = Formula({"L"}, lambda m: m["L"])


KB = [
    R_implies_W,
    S_implies_W,
    W_implies_L,
    C_implies_R,
    S_or_C,
    S_equiv_D
]


result = entails(KB, Query_L)
print("\nDoes KB entail L (grass is slippery)? →", result)
