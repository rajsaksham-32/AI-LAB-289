# ----------------------------------------------------
# First Order Logic Resolution Prover (Corrected)
# ----------------------------------------------------

import copy

def is_variable(x):
    return isinstance(x, str) and x[0].islower()

def unify(x, y, theta=None):
    if theta is None:
        theta = {}
    if theta == "FAIL":
        return "FAIL"
    elif x == y:
        return theta
    elif is_variable(x):
        return unify_var(x, y, theta)
    elif is_variable(y):
        return unify_var(y, x, theta)
    elif isinstance(x, list) and isinstance(y, list) and len(x) == len(y):
        return unify(x[1:], y[1:], unify(x[0], y[0], theta))
    else:
        return "FAIL"

def unify_var(var, x, theta):
    if var in theta:
        return unify(theta[var], x, theta)
    elif x in theta:
        return unify(var, theta[x], theta)
    else:
        if occurs_check(var, x, theta):
            return "FAIL"
        theta_copy = theta.copy()
        theta_copy[var] = x
        return theta_copy

def occurs_check(var, x, theta):
    if var == x:
        return True
    elif isinstance(x, list):
        return any(occurs_check(var, arg, theta) for arg in x)
    elif isinstance(x, str) and x in theta:
        return occurs_check(var, theta[x], theta)
    return False

# -------------------------------------------------
# Resolution Utilities
# -------------------------------------------------

def substitute(theta, clause):
    new_clause = []
    for pred in clause:
        name = pred[0]
        args = pred[1]
        new_args = [(theta[arg] if arg in theta else arg) for arg in args]
        new_clause.append([name, new_args])
    return new_clause


def resolve(ci, cj):
    resolvents = []

    for pi in ci:
        for pj in cj:
 
            if pi[0] == "~" + pj[0] or pj[0] == "~" + pi[0]:
                theta = unify(pi[1], pj[1], {})
                if theta != "FAIL":

                    ci_new = substitute(theta, [x for x in ci if x != pi])
                    cj_new = substitute(theta, [x for x in cj if x != pj])

                    resolvent = []
                    for term in ci_new + cj_new:
                        if term not in resolvent:
                            resolvent.append(term)

                    resolvents.append(resolvent)

    return resolvents


def clause_to_hashable(clause):
    """
    clause = [["Pred", ["a","b"]], ["~Q", ["x"]]]
    → (("Pred", ("a","b")), ("~Q", ("x",)))
    """
    return tuple((pred[0], tuple(pred[1])) for pred in clause)


def hashable_to_clause(tup):
    """ reverse conversion """
    return [[pred, list(args)] for pred, args in tup]




def resolution_algorithm(KB, query):

    KB = copy.deepcopy(KB)

    neg_query = []
    for q in query:
        if q[0].startswith("~"):
            neg_query.append([q[0][1:], q[1]])
        else:
            neg_query.append(["~" + q[0], q[1]])
    KB.append(neg_query)

    print("\nInitial KB + neg(query):")
    for c in KB:
        print(c)

    new = set()

    while True:


        pairs = [(KB[i], KB[j]) for i in range(len(KB)) for j in range(i+1, len(KB))]

        for (ci, cj) in pairs:
            resolvents = resolve(ci, cj)

            for r in resolvents:

                if r == []:
                    print("\n❗ Contradiction found → QUERY PROVED.\n")
                    return True

                r_hash = clause_to_hashable(r)

                if r_hash not in new:
                    new.add(r_hash)

 
        if all(hashable_to_clause(r) in KB for r in new):
            print("\nNo new clauses → QUERY NOT PROVED.\n")
            return False


        for r in new:
            clause = hashable_to_clause(r)
            if clause not in KB:
                KB.append(clause)




KB = [
    [["Parent", ["x", "y"]], ["~Mother", ["x", "y"]]], 
    [["Mother", ["Mary", "John"]]]
]

query = [["Parent", ["Mary", "John"]]]

print("Trying to prove:", query)
resolution_algorithm(KB, query)
