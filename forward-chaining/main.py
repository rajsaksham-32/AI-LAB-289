from copy import deepcopy
def occurs_check(var, expr):
    if var == expr:
        return True
    elif isinstance(expr, list):
        return any(occurs_check(var, subexpr) for subexpr in expr)
    return False

def substitute(expr, subst):
    if isinstance(expr, str):
        return subst.get(expr, expr)
    elif isinstance(expr, list):
        return [substitute(e, subst) for e in expr]
    return expr
def unify(x, y, subst=None):
    if subst is None:
        subst = {}
    if subst is None:
        return None
    if x == y:
        return subst
    elif isinstance(x, str) and x.islower():  
        if x in subst:
            return unify(subst[x], y, subst)
        elif occurs_check(x, y):
            return None
        else:
            subst[x] = y
            return subst
    elif isinstance(y, str) and y.islower():  
        return unify(y, x, subst)
    elif isinstance(x, list) and isinstance(y, list) and len(x) == len(y):
        for a, b in zip(x, y):
            subst = unify(a, b, subst)
            if subst is None:
                return None
        return subst
    else:
        return None

def parse_sentence(sentence):
    """Parse sentence like 'Parent(John, x)' → ['Parent', 'John', 'x']"""
    sentence = sentence.strip()
    if '(' in sentence and ')' in sentence:
        pred = sentence[:sentence.index('(')]
        args = sentence[sentence.index('(') + 1:sentence.index(')')].split(',')
        args = [a.strip() for a in args]
        return [pred] + args
    else:
        return [sentence]

def to_string(expr):
    if len(expr) == 1:
        return expr[0]
    else:
        return f"{expr[0]}({', '.join(expr[1:])})"
def fol_fc_ask(KB, query):
    print("FORWARD CHAINING START ")
    print("Initial Knowledge Base:")
    for fact in KB:
        print("   ", fact)
    print("Query:", query)
    

    iteration = 0
    new = set()

    while True:
        iteration += 1
        print(f"\n--- Iteration {iteration} ---")
        n_new = set()

        for rule in KB.copy():
            if "=>" in rule:
                premise, conclusion = rule.split("=>")
                premise = premise.strip()
                conclusion = conclusion.strip()
                premises = [p.strip() for p in premise.split("^")]

                print(f"\nChecking rule: {rule}")

                substitutions = []
           
                for fact in KB:
                    if "=>" not in fact:
                        for p in premises:
                            s = unify(parse_sentence(p), parse_sentence(fact))
                            if s is not None:
                                print(f"  Premise '{p}' unified with fact '{fact}' using {s}")
                                substitutions.append(s)

        
                for s in substitutions:
                    new_fact = to_string(substitute(parse_sentence(conclusion), s))
                    if new_fact not in KB and new_fact not in n_new:
                        print(f"  => New fact inferred: {new_fact}")
                        n_new.add(new_fact)
                        phi = unify(parse_sentence(new_fact), parse_sentence(query))
                        if phi is not None:
                            print("\n Query proved!")
                            print(f"Substitution set: {phi}")
                            return phi

        if not n_new:
            print("\nNo new inferences. Forward chaining ends.")
            print("Query cannot be proved.")
            return False

        print("\nNewly inferred facts this iteration:")
        for fact in n_new:
            print("   ", fact)

        KB |= n_new
        print("\nUpdated Knowledge Base:")
        for fact in KB:
            print("   ", fact)

KB = {
    "Parent(John, Mary)",
    "Parent(Mary, Alice)",
    "Parent(x, y) ^ Parent(y, z) => Grandparent(x, z)"
}

query = "Grandparent(John, Alice)"

result = fol_fc_ask(deepcopy(KB), query)
