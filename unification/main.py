def occurs_check(var, expr):
    if var == expr:
        return True
    elif isinstance(expr, list):
        return any(occurs_check(var, subexpr) for subexpr in expr)
    return False


def unify(x, y, subst=None):
    if subst is None:
        subst = {}

    if isinstance(x, str) and x.islower():  
        if x in subst:
            return unify(subst[x], y, subst)
        elif occurs_check(x, y):
            return None
        else:
            subst[x] = y
            return subst

    elif isinstance(y, str) and y.islower():  
        if y in subst:
            return unify(x, subst[y], subst)
        elif occurs_check(y, x):
            return None
        else:
            subst[y] = x
            return subst

    elif x == y:
        return subst

    elif isinstance(x, list) and isinstance(y, list):
        if len(x) != len(y):
            return None
        for xi, yi in zip(x, y):
            subst = unify(xi, yi, subst)
            if subst is None:
                return None
        return subst

    else:
        return None



expr1 = ["Knows", "John", "x"]
expr2 = ["Knows", "y", "Mary"]

print("Expression 1:", expr1)
print("Expression 2:", expr2)

result = unify(expr1, expr2)
if result:
    for k, v in result.items():
        print(f"{k} / {v}")
else:
    print("Unification failed.")
