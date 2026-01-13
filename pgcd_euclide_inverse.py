def sep(title=None):
    if title:
        print("--- {} ---".format(title))
    else:
        print("-" * 38)

def show_divisions(divs):
    for (A, B, q, r) in divs:
        print("{} = {}*{} + {}".format(A, q, B, r))

def _expr_to_string(expr, R):
    terms = []
    for i in range(len(R)):
        c = expr.get(i, 0)
        if c != 0:
            terms.append("{}*{}".format(c, R[i]))
    if not terms:
        return "0"
    return " + ".join(terms)

def gcd(a, b):
    a = abs(a); b = abs(b)
    while b:
        a, b = b, a % b
    return a

def egcd_verbose(a, b, show=True, show_back=True):
    A0, B0 = a, b
    divs = []
    R = [a, b]
    Q = [None, None]

    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1

    while r != 0:
        q = old_r // r
        rem = old_r - q * r
        divs.append((old_r, r, q, rem))
        R.append(rem)
        Q.append(q)
        old_r, r = r, rem
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t

    g, x, y = old_r, old_s, old_t
    k = len(R) - 2

    if show:
        sep("Algorithme d'Euclide ({} , {})".format(A0, B0))
        show_divisions(divs)
        print("pgcd({}, {}) = {}".format(A0, B0, g))

    if show and show_back and k >= 2:
        sep("Remontée (U,V) : {} = U*a + V*b".format(g))
        print("{} = {} - {}*{}".format(R[k], R[k-2], Q[k], R[k-1]))
        expr = {k-2: 1, k-1: -Q[k]}
        for j in range(k-1, 1, -1):
            cj = expr.get(j, 0)
            if cj == 0:
                continue
            expr.pop(j, None)
            expr[j-2] = expr.get(j-2, 0) + cj
            expr[j-1] = expr.get(j-1, 0) - cj * Q[j]
            print("=> {} = {}".format(R[k], _expr_to_string(expr, R)))
        U = expr.get(0, 0)
        V = expr.get(1, 0)
        print("Donc {} = {}*{} + {}*{}".format(g, U, A0, V, B0))

    if show:
        print("Coeffs de Bézout : U = {}, V = {}".format(x, y))
        print("Vérif : {}*{} + {}*{} = {}".format(A0, x, B0, y, A0*x + B0*y))
    return g, x, y

def inv_mod(a, m, show=True):
    if m <= 0:
        if show:
            print("Le module doit être > 0")
        return False, None
    g, x, y = egcd_verbose(a, m, show=show, show_back=True)
    if g != 1:
        if show:
            sep("Inverse modulaire")
            print("pgcd({}, {}) = {} ≠ 1 : pas d'inverse modulo {}.".format(a, m, g, m))
        return False, None
    inv = x % m
    if show:
        sep("Inverse mod {}".format(m))
        print("Inverse trouvé : {}^(-1) ≡ {}  [ {} ]".format(a, inv, m))
        print("Vérif : ({}*{}) % {} = {}".format(a, inv, m, (a*inv) % m))
    return True, inv

def run_pgcd_simple():
    sep("PGCD (simple)")
    try:
        a = int(input("a = "))
        b = int(input("b = "))
    except:
        print("Entrée invalide.")
        return
    g = gcd(a, b)
    print("pgcd({}, {}) = {}".format(a, b, g))

def run_euclide_bezout():
    sep("Euclide étendu (U,V) + Bézout")
    try:
        a = int(input("a = "))
        b = int(input("b = "))
    except:
        print("Entrée invalide.")
        return
    egcd_verbose(a, b, show=True, show_back=True)

def run_inverse_mod():
    sep("Inverse modulaire")
    try:
        a = int(input("a = "))
        m = int(input("m (module > 0) = "))
    except:
        print("Entrée invalide.")
        return
    inv_mod(a, m, show=True)

def menu():
    sep("MENU")
    print("1) PGCD (simple)")
    print("2) Euclide étendu (U,V) + Bézout")
    print("3) Inverse mod m")
    print("4) Quitter")
    choice = input("> Choix : ").strip()

    if choice == "1":
        run_pgcd_simple()
    elif choice == "2":
        run_euclide_bezout()
    elif choice == "3":
        run_inverse_mod()
    elif choice == "4":
        print("Quitter le programme.")
        return
    else:
        print("Choix inconnu.")

menu()
