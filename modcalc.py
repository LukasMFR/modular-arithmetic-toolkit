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

def _rjust(val, w):
    s = str(val)
    L = len(s)
    if L < w:
        return " " * (w - L) + s
    return s

def _col_width(values):
    w = 1
    for v in values:
        l = len(str(v))
        if l > w:
            w = l
    return w + 1

def _print_table(header_vals, row_vals, cell_fn, title):
    sep(title)
    candidates = list(header_vals) + list(row_vals)
    for i in row_vals:
        for j in header_vals:
            candidates.append(cell_fn(i, j))
    w = _col_width(candidates)

    first_cell = " " * w + "|"
    print(first_cell, end="")
    for j in header_vals:
        print(_rjust(j, w), end="")
    print()

    print("-" * (w + 1 + w * len(header_vals)))

    for i in row_vals:
        print(_rjust(i, w) + "|", end="")
        for j in header_vals:
            v = cell_fn(i, j)
            print(_rjust(v, w), end="")
        print()

def gcd(a, b):
    a = abs(a); b = abs(b)
    while b:
        a, b = b, a % b
    return a

def _format_factorization(fdict):
    parts = []
    for p in sorted(fdict.keys()):
        e = fdict[p]
        if e == 1:
            parts.append(str(p))
        else:
            parts.append("{}^{}".format(p, e))
    return " * ".join(parts) if parts else "1"

def prime_factors_ladder(n):
    if n == 0:
        print("0 : factorisation non définie (multiple de tous les entiers).")
        return {}
    sign = -1 if n < 0 else 1
    if sign < 0:
        print("Attention: n < 0 -> on factorise |n| et on garde le signe -1.")
    n = abs(n)
    if n == 1:
        print("1")
        return {}

    print(n)
    f = {}

    while n % 2 == 0:
        n //= 2
        print("{} | {}".format(n, 2))
        f[2] = f.get(2, 0) + 1

    p = 3
    while p * p <= n:
        while n % p == 0:
            n //= p
            print("{} | {}".format(n, p))
            f[p] = f.get(p, 0) + 1
        p += 2

    if n > 1:
        print("1 | {}".format(n))
        f[n] = f.get(n, 0) + 1

    return f if sign > 0 else ({-1:1} | f) if hasattr(dict, "__or__") else (dict([(-1,1)]) | f)

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
        sep("Remontée (combinaison linéaire)")
        print("{} = {} - {}*{}".format(R[k], R[k-2], Q[k], R[k-1]))
        expr = {k-2: 1, k-1: -Q[k]}
        for j in range(k-1, 1, -1):
            cj = expr.get(j, 0)
            if cj == 0:
                continue
            print("Remplacer {} par {} - {}*{}".format(R[j], R[j-2], Q[j], R[j-1]))
            expr.pop(j, None)
            expr[j-2] = expr.get(j-2, 0) + cj
            expr[j-1] = expr.get(j-1, 0) - cj * Q[j]
            print("=> {} = {}".format(R[k], _expr_to_string(expr, R)))
        x_back = expr.get(0, 0)
        y_back = expr.get(1, 0)
        print("Donc {} = {}*{} + {}*{}".format(g, x_back, A0, y_back, B0))

    if show:
        print("Coeffs de Bézout : x = {}, y = {}".format(x, y))
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
            print("gcd({}, {}) = {} ≠ 1 : pas d'inverse modulo {}.".format(a, m, g, m))
        return False, None
    inv = x % m
    if show:
        sep("Inverse mod {}".format(m))
        print("Inverse trouvé : {}^(-1) ≡ {}  [ {} ]".format(a, inv, m))
        print("Vérif : ({}*{}) % {} = {}".format(a, inv, m, (a*inv) % m))
    return True, inv

def solve_congruence(a, b, m, show=True, list_rep=True):
    if m <= 0:
        if show:
            print("Le module doit être > 0")
        return False, None, None, None
    sep("Résolution de {} x ≡ {}  [ {} ]".format(a, b, m))
    d, xg, yg = egcd_verbose(a, m, show=True, show_back=False)
    if b % d != 0:
        print("Comme {} ne divise pas {}, aucune solution.".format(d, b))
        return False, None, None, d
    a1 = a // d; b1 = b // d; m1 = m // d
    print("On réduit : a'={}, b'={}, m'={} (d = {})".format(a1, b1, m1, d))
    print("Nouvelle équation : {} x ≡ {}  [ {} ]".format(a1, b1, m1))
    ok, inv = inv_mod(a1, m1, show=True)
    if not ok:
        print("Problème inattendu : a' et m' ne sont pas copremiers.")
        return False, None, None, d
    x0 = (inv * b1) % m1
    sep("Solution")
    print("Solution de base : x0 ≡ {} * {} ≡ {}  [ {} ]".format(inv, b1, x0, m1))
    print("Vérif : ({}*{}) % {} = {}  (doit ≡ {})".format(a, x0, m, (a*x0) % m, b % m))
    print("Forme générale des solutions : x ≡ {}  [ {} ]".format(x0, m1))
    if d > 1:
        k_values = ", ".join(str(i) for i in range(d))
        print("Remontée au mod {} : x ≡ {} + {}k, k = {}.".format(m, x0, m1, k_values))
        reps = []
        for k in range(d):
            reps.append((x0 + k*m1) % m)
        reps = sorted(list(set(reps)))
        if list_rep:
            print("Représentants (mod {}): {}".format(m, ", ".join(str(r) for r in reps)))
    return True, x0, m1, d

def solve_ax_plus_c_eq_b(a, c, b, m):
    sep("0) Mise en forme / réduction modulo {}".format(m))
    if (b % m) == 0 and (c % m) != 0:
        print("{} x ≡ -{} ≡ {}  [ {} ]".format(a, c, (-c) % m, m))
    elif (c % m) == 0:
        print("{} x ≡ {}  [ {} ]".format(a, b % m, m))
    else:
        print("{} x ≡ {} - {} ≡ {}  [ {} ]".format(a, b % m, c % m, (b - c) % m, m))
    return solve_congruence(a, (b - c) % m, m, show=True, list_rep=True)

def solve_x_plus_c_eq_b(c, b, m):
    sep("0) Mise en forme / réduction modulo {}".format(m))
    print("{} ≡ {}  [ {} ]".format(c, c % m, m))
    print("{} ≡ {}  [ {} ]".format(b, b % m, m))
    print("=> x ≡ {}  [ {} ]".format((b - c) % m, m))
    return solve_congruence(1, (b - c) % m, m, show=True, list_rep=True)

def equations_menu_option():
    sep("Équations - choisir une forme")
    print("1) a x ≡ b  [ m ]")
    print("2) a x + c ≡ 0  [ m ]")
    print("3) a x + c ≡ b  [ m ]")
    print("4) x + c ≡ b  [ m ]")
    ch = input("> Choix forme : ").strip()

    try:
        if ch == "1":
            a = int(input("a = "))
            b = int(input("b = "))
            m = int(input("m (module > 0) = "))
            solve_congruence(a, b, m, show=True, list_rep=True)

        elif ch == "2":
            a = int(input("a = "))
            c = int(input("c = "))
            m = int(input("m (module > 0) = "))
            sep("Équation {}x + {} = 0  [ {} ]".format(a, c, m))
            print("Réécriture : {}x ≡ -{} ≡ {}  [ {} ]".format(a, c, (-c) % m, m))
            solve_congruence(a, (-c) % m, m, show=True, list_rep=True)

        elif ch == "3":
            a = int(input("a = "))
            c = int(input("c = "))
            b = int(input("b = "))
            m = int(input("m (module > 0) = "))
            solve_ax_plus_c_eq_b(a, c, b, m)

        elif ch == "4":
            c = int(input("c = "))
            b = int(input("b = "))
            m = int(input("m (module > 0) = "))
            solve_x_plus_c_eq_b(c, b, m)

        else:
            print("Choix inconnu.")
    except:
        print("Entrée invalide.")

def table_Z(start, end, op):
    if start > end:
        start, end = end, start
    rows = list(range(start, end + 1))
    cols = list(range(start, end + 1))
    if op == "+":
        cell = lambda i, j: i + j
        title = "Table d'addition en Z, [{}..{}]".format(start, end)
    else:
        cell = lambda i, j: i * j
        title = "Table de multiplication en Z, [{}..{}]".format(start, end)
    _print_table(cols, rows, cell, title)

def table_Zn(n, op):
    if n <= 0:
        print("Le module n doit être > 0")
        return
    rows = list(range(0, n))
    cols = list(range(0, n))
    if op == "+":
        cell = lambda i, j: (i + j) % n
        title = "Table d'addition modulo {}".format(n)
    else:
        cell = lambda i, j: (i * j) % n
        title = "Table de multiplication modulo {}".format(n)
    _print_table(cols, rows, cell, title)

    Zn_list = [i for i in range(n)]
    print("\nZ_{} = {{ {} }}".format(n, ", ".join([str(x) for x in Zn_list])))
    Zn_star = [a for a in range(n) if gcd(a, n) == 1]
    print("Z_{}* = {{ {} }}".format(n, ", ".join([str(x) for x in Zn_star])))

def solve_system_crt_coprime():
    sep("CRT (formule directe)")
    k = int(input("Nombre d'équations k = "))
    if k <= 0:
        print("k doit être >= 1")
        return

    residues = []
    moduli = []
    for i in range(1, k+1):
        print("Equation #{} :".format(i))
        ai = int(input("  a{} = ".format(i)))
        mi = int(input("  m{} (>0) = ".format(i)))
        if mi <= 0:
            print("Module > 0 requis.")
            return
        ai = ai % mi
        residues.append(ai)
        moduli.append(mi)

    for i in range(k):
        for j in range(i+1, k):
            if gcd(moduli[i], moduli[j]) != 1:
                print("Moduli NON copremiers (m{}={}, m{}={}).".format(i+1, moduli[i], j+1, moduli[j]))
                print("Utilise l'option (6) Système modulaire (cas général).")
                return

    print("Système :")
    for i in range(k):
        print("x ≡ {}  [ {} ]".format(residues[i], moduli[i]))

    M = 1
    for mi in moduli:
        M *= mi
    sep("Produit total")
    prod_str = " * ".join(str(mi) for mi in moduli)
    print("M = {} = {}".format(prod_str, M))

    sep("Sous-produits")
    Mi_list = []
    for i in range(k):
        Mi = M // moduli[i]
        Mi_list.append(Mi)
        print("M{} = M / m{} = {}".format(i+1, i+1, Mi))

    sep("Recherche des inverses (Mi * yi ≡ 1 [mi])")
    yi_list = []
    for i in range(k):
        Mi = Mi_list[i]
        mi = moduli[i]
        r = Mi % mi
        ok, yi = inv_mod(Mi, mi, show=False)
        if not ok:
            print("Impossible de trouver l'inverse de {} modulo {} (devrait être possible ici).".format(Mi, mi))
            return
        yi_list.append(yi)
        print("{}*y{} ≡ 1 [{}] -> {} ≡ {} [{}] -> y{} ≡ {} [{}] => y{} = {}".format(
            Mi, i+1, mi, Mi, r, mi, i+1, yi, mi, i+1, yi
        ))

    sep("Construction (formule CRT)")
    terms_str = "  +  ".join("{} * {} * {}".format(residues[i], Mi_list[i], yi_list[i]) for i in range(k))
    print("x ≡ {}  [ {} ]".format(terms_str, M))

    sep("Calcul des termes")
    terms = []
    for i in range(k):
        t = residues[i] * Mi_list[i] * yi_list[i]
        terms.append(t)
        print("Terme #{} = {}*{}*{} = {}".format(i+1, residues[i], Mi_list[i], yi_list[i], t))

    sep("Somme")
    S = sum(terms)
    print("S = {}".format(" + ".join(str(t) for t in terms)), end="")
    print(" = {}".format(S))
    sep("Réduction")
    x0 = S % M
    print("x0 = {} % {} = {}".format(S, M, x0))

    sep("Solution canonique")
    print("x ≡ {}  [ {} ]".format(x0, M))

    sep("Vérifications")
    for i in range(k):
        mi = moduli[i]
        ai = residues[i]
        print("{} % {} = {}  (attendu {}){}".format(
            x0, mi, x0 % mi, ai, "  (ok)" if (x0 % mi) == ai else "  (!!)"
        ))

    sep("Forme générale")
    print("x = {} + {}*k,  k entier".format(x0, M))

def pow_mod_verbose(a, e, m):
    sep('Puissance mod m - méthode "décomposition binaire"')

    if m <= 0:
        print("Le module doit être > 0")
        return None
    if e < 0:
        print("Exposant négatif non pris en charge.")
        return None
    if e == 0:
        print("Objectif : calculer {}^0  [{}]".format(a, m))
        print("{}^0 ≡ 1  [{}]".format(a, m))
        sep("Résultat")
        print("{}^{} (mod {}) = {}".format(a, e, m, 1 % m))
        return 1 % m

    print("a = {}".format(a))
    print("e = {}".format(e))
    print("m = {}".format(m))
    print("\nObjectif : calculer {}^{}  [{}]".format(a, e, m))

    orig_e = e
    is_prime = True
    if m < 2:
        is_prime = False
    else:
        d = 2
        while d * d <= m:
            if m % d == 0:
                is_prime = False
                break
            d += 1

    if is_prime and gcd(a, m) == 1 and e >= (m - 1):
        sep("Réduction de l'exposant (th. de Fermat)")
        print("m = {} est premier et gcd({}, {}) = 1.".format(m, a, m))
        print("On sait : {}^({}-1) ≡ 1  [ {} ]".format(a, m, m))
        r = e % (m - 1)
        q = e // (m - 1)
        print("On écrit e = q*({}-1) + r avec e = {} :".format(m, orig_e))
        print("{} = {} * {} + {}.".format(orig_e, q, m - 1, r))
        print("Donc {}^{} ≡ {}^{}  [ {} ]".format(a, orig_e, a, r, m))
        e = r
        if e == 0:
            sep("Résultat")
            print("{}^{} (mod {}) = 1".format(a, orig_e, m))
            print("(Car l'exposant est multiple de {}-1 et {}^({}-1) ≡ 1 [ {} ])".format(m, a, m, m))
            return 1

    def small_rep(x, mod):
        return str(x % mod)

    def power2_repr(a_sym, k):
        if k == 0:
            return "{}".format(a_sym)
        s = "({}^2)".format(a_sym)
        for _ in range(1, k):
            s = "({}^2)".format(s)
        return s

    bits = []
    k = 0
    t = e
    while t > 0:
        if (t & 1) == 1:
            bits.append(k)
        t >>= 1
        k += 1
    bits_desc = sorted(bits, reverse=True)

    somme_num = " + ".join(str(1 << k) for k in bits_desc)
    somme_pow2 = " + ".join("2^{}".format(k) for k in bits_desc)
    print("\n1) Écriture de l'exposant en base 2")
    print("{} = {} = {}".format(e, somme_num, somme_pow2))

    print("\n2) Décomposition de la puissance")
    droite_pow2 = " + ".join("2^{}".format(k) for k in bits_desc)
    print("{}^{} = {}^({})".format(a, e, a, droite_pow2))
    print("     = " + " * ".join("{}^(2^{})".format(a, k) for k in bits_desc))

    print("\n3) Calculs modulo {} (paliers)".format(m))
    pow_values = {}

    val = a % m
    pow_values[0] = val
    print("- {}^1 ≡ {}  [ {} ]".format(a, small_rep(a, m), m))

    max_k = bits_desc[0] if bits_desc else 0
    prev_val = val
    for kk in range(1, max_k + 1):
        raw_sq = prev_val * prev_val
        new_val = raw_sq % m
        exp_prev = 1 << (kk - 1)
        exp_cur = 1 << kk
        print("- {}^{} = ({}^{})^2  =>  ({}^2) ≡ {}  [ {} ]".format(
            a,
            exp_cur,
            a,
            exp_prev,
            small_rep(prev_val, m),
            small_rep(new_val, m),
            m
        ))
        pow_values[kk] = new_val
        prev_val = new_val

    print("\n4) Assemblage des facteurs utiles ({})".format(", ".join("2^{}".format(k) for k in bits_desc)))
    print("{}^{} ≡ {}  [ {} ]".format(
        a, e, " * ".join("{}^(2^{})".format(a, k) for k in bits_desc), m
    ))
    factors_str = " * ".join(small_rep(pow_values[k], m) for k in bits_desc)
    print("     ≡ {}  [ {} ]".format(factors_str, m))

    acc = 1 % m
    if bits_desc:
        acc = pow_values[bits_desc[0]] % m
        print("     -> {} (premier facteur)".format(small_rep(acc, m)))
        for kk in bits_desc[1:]:
            before = acc
            acc = (acc * pow_values[kk]) % m
            print("     -> ({} * {}) % {} = {}".format(
                small_rep(before, m),
                small_rep(pow_values[kk], m),
                m,
                small_rep(acc, m)
            ))

    sep("Résultat")
    print("{}^{} (mod {}) = {}".format(a, orig_e, m, acc))
    print("(Vérif rapide : {} % {} = {})".format(acc, m, acc % m))
    return acc

def show_factorization_and_option_gcd():
    sep("Décomp. facteurs premiers")
    k = int(input("Nombre d'entiers (1 ou 2) = "))
    if k not in (1, 2):
        print("Choix invalide (1 ou 2).")
        return

    n1 = int(input("n1 = "))
    sep("n1 : échelle")
    f1 = prime_factors_ladder(n1)
    absn1 = abs(n1)
    print("{} = {}".format(n1, _format_factorization({p:e for p,e in f1.items() if p != -1} if -1 in f1 else f1)))

    if k == 1:
        return

    n2 = int(input("n2 = "))
    sep("n2 : échelle")
    f2 = prime_factors_ladder(n2)
    print("{} = {}".format(n2, _format_factorization({p:e for p,e in f2.items() if p != -1} if -1 in f2 else f2)))

    sep("PGCD par facteurs")
    f1pos = {p:e for p,e in f1.items() if p > 1}
    f2pos = {p:e for p,e in f2.items() if p > 1}
    common = {}
    for p in f1pos:
        if p in f2pos:
            common[p] = min(f1pos[p], f2pos[p])

    pgcd_val = 1
    for p, e in common.items():
        v = 1
        for _ in range(e):
            v *= p
        pgcd_val *= v

    if common:
        fact_str = _format_factorization(common)
        print("PGCD({}, {}) = {} = {}".format(n1, n2, fact_str, pgcd_val))
    else:
        print("PGCD({}, {}) = 1".format(n1, n2))

def run_pgcd_bezout():
    sep("PGCD / Bézout")
    try:
        a = int(input("a = "))
        b = int(input("b = "))
        egcd_verbose(a, b, show=True, show_back=True)
    except:
        print("Entrée invalide.")

def run_inverse():
    sep("Inverse mod m")
    try:
        a = int(input("a = "))
        m = int(input("m (module > 0) = "))
        inv_mod(a, m, show=True)
    except:
        print("Entrée invalide.")

def run_tables():
    sep("Tables (Z / Z_n)")
    try:
        print("Espace ?")
        print("  1 = Z (entiers)")
        print("  2 = Z_n (modulo n)")
        space = input("> Choix espace : ").strip()

        print("Opération ?")
        print("  1 = addition")
        print("  2 = multiplication")
        print("  3 = les deux")
        op_ch = input("> Choix opération : ").strip()

        def do_ops(do_add, do_mul, in_Z, in_Zn):
            if in_Z:
                print("Intervalle en Z :")
                s = int(input("  début = "))
                e = int(input("  fin   = "))
                if do_add: table_Z(s, e, "+")
                if do_mul: table_Z(s, e, "*")
            else:
                n = int(input("Module n (>0) : "))
                if do_add: table_Zn(n, "+")
                if do_mul: table_Zn(n, "*")

        do_add = (op_ch == "1" or op_ch == "3")
        do_mul = (op_ch == "2" or op_ch == "3")

        if space == "1":
            do_ops(do_add, do_mul, True, False)
        elif space == "2":
            do_ops(do_add, do_mul, False, True)
        else:
            print("Choix d'espace invalide.")
    except:
        print("Entrée invalide.")

def run_pow_mod():
    sep("Puissance mod m")
    try:
        a = int(input("a = "))
        e = int(input("e (exposant) = "))
        m = int(input("m (module > 0) = "))
        pow_mod_verbose(a, e, m)
    except:
        print("Entrée invalide.")

def _mul_mod_verbose(a, b, m, label=None):
    if label:
        sep(label)
    prod = a * b
    print("{} * {} = {}".format(a, b, prod))
    r = prod % m
    print("{} mod {} = {}".format(prod, m, r))
    return r

def _rsa_system(name, p, q, e):
    sep("RSA - Paramètres {}".format(name))
    print("p = {}, q = {}, e = {}".format(p, q, e))
    n = p * q
    phi = (p - 1) * (q - 1)
    print("n = p*q = {}*{} = {}".format(p, q, n))
    print("phi(n) = (p-1)(q-1) = {}*{} = {}".format(p-1, q-1, phi))
    sep("Calcul de d : d ≡ e^(-1) [phi(n)]")
    ok, d = inv_mod(e, phi, show=True)
    if not ok:
        print("ERREUR: e et phi(n) ne sont pas copremiers, RSA invalide.")
        return None
    sep("Clés {}".format(name))
    print("Clé publique  : (n, e) = ({}, {})".format(n, e))
    print("Clé privée    : (n, d) = ({}, {})".format(n, d))
    return {"name": name, "p": p, "q": q, "n": n, "phi": phi, "e": e, "d": d}

def _rsa_encrypt_for_bob(M, bob):
    sep("RSA - Chiffrement pour Bob")
    print("C(M) = M^e_B mod n_B")
    print("M = {}, e_B = {}, n_B = {}".format(M, bob["e"], bob["n"]))
    C = pow_mod_verbose(M, bob["e"], bob["n"])
    return C

def _rsa_decrypt_by_bob(C, bob):
    sep("RSA - Déchiffrement par Bob")
    print("M = C^d_B mod n_B")
    print("C = {}, d_B = {}, n_B = {}".format(C, bob["d"], bob["n"]))
    M = pow_mod_verbose(C, bob["d"], bob["n"])
    return M

def _rsa_sign_by_alice_on_cipher(Cm, alice):
    sep("RSA - Signature par Alice (sur le chiffré)")
    print("sigma = C(m)^(d_A) mod n_A")
    print("C(m) = {}, d_A = {}, n_A = {}".format(Cm, alice["d"], alice["n"]))
    sigma = pow_mod_verbose(Cm, alice["d"], alice["n"])
    return sigma

def _rsa_verify_by_bob(Cm, sigma, alice):
    sep("RSA - Vérification de la signature (côté Bob)")
    print("On vérifie : C(m) ?= sigma^(e_A) mod n_A")
    print("C(m) = {}, sigma = {}, e_A = {}, n_A = {}".format(Cm, sigma, alice["e"], alice["n"]))
    v = pow_mod_verbose(sigma, alice["e"], alice["n"])
    sep("Conclusion vérif")
    if v == (Cm % alice["n"]):
        print("OK : {} == {} -> signature valide (message bien lié à Alice)".format(v, Cm % alice["n"]))
    else:
        print("NON : {} != {} -> signature invalide".format(v, Cm % alice["n"]))
    return v

def ds_rsa_ex1_run(choice):
    pA, qA, eA = 11, 19, 7
    pB, qB, eB = 13, 17, 5
    M = 42
    m = 2

    alice = _rsa_system("Alice", pA, qA, eA)
    bob   = _rsa_system("Bob",   pB, qB, eB)
    if not alice or not bob:
        return

    if choice in ("1", "5"):
        sep("Ex1 Q1+Q2 - Résumé à recopier")
        print("Alice: n_A = {}, phi_A = {}, e_A = {}, d_A = {}".format(alice["n"], alice["phi"], alice["e"], alice["d"]))
        print("Bob  : n_B = {}, phi_B = {}, e_B = {}, d_B = {}".format(bob["n"], bob["phi"], bob["e"], bob["d"]))

    if choice in ("2", "5"):
        sep("Ex1 Q3 - Chiffrer M=42 pour Bob")
        C_M = _rsa_encrypt_for_bob(M, bob)
        sep("Résultat Q3")
        print("C(M) = {}".format(C_M))

    if choice in ("3", "5"):
        sep("Ex1 Q4 - m=2 + signature numérique (sur C(m))")
        Cm = _rsa_encrypt_for_bob(m, bob)
        sep("Chiffré du message m")
        print("C(m) = {}".format(Cm))
        sigma = _rsa_sign_by_alice_on_cipher(Cm, alice)
        sep("Résultat Q4.1")
        print("Signature sigma = {}".format(sigma))

    if choice in ("4", "5"):
        sep("Ex1 Q5 - Réception (déchiffrement + authenticité)")
        Cm = _rsa_encrypt_for_bob(m, bob)
        sigma = _rsa_sign_by_alice_on_cipher(Cm, alice)

        sep("Q5.1 Déchiffrement")
        m_back = _rsa_decrypt_by_bob(Cm, bob)
        sep("Résultat Q5.1")
        print("Message déchiffré = {}".format(m_back))

        sep("Q5.2 Vérification signature")
        _rsa_verify_by_bob(Cm, sigma, alice)

def rsa_ds_menu():
    sep("DS - EXERCICE 1 (RSA)")
    print("1) Q1+Q2 (n, phi, clés)")
    print("2) Q3 (chiffrer M=42 -> C(M))")
    print("3) Q4 (m=2, calcul C(m) + signature)")
    print("4) Q5 (déchiffrer + vérifier signature)")
    print("5) Tout l'exercice 1")
    print("6) Retour")
    ch = input("> Choix : ").strip()
    if ch in ("1", "2", "3", "4", "5"):
        ds_rsa_ex1_run(ch)

def _elgamal_public_y(g, a, p, who):
    sep("ElGamal - Clé publique {}".format(who))
    print("y = g^clé_privée mod p")
    y = pow_mod_verbose(g, a, p)
    return y

def _elgamal_encrypt(M, p, g, a_alice, b_bob):
    sep("ElGamal - Chiffrement (Ex2 Q2)")
    print("p = {}, g = {}, M = {}".format(p, g, M))
    print("Alice: a = {} ; Bob: b = {}".format(a_alice, b_bob))

    yB = _elgamal_public_y(g, b_bob, p, "Bob (yB)")
    sep("C1 = g^a mod p")
    C1 = pow_mod_verbose(g, a_alice, p)

    sep("s = (yB)^a mod p")
    s_shared = pow_mod_verbose(yB, a_alice, p)

    sep("C2 = M * s mod p")
    C2 = _mul_mod_verbose(M, s_shared, p, label=None)

    sep("Chiffré (C1, C2)")
    print("(C1, C2) = ({}, {})".format(C1, C2))
    return C1, C2, yB, s_shared

def _elgamal_decrypt(C1, C2, p, b_bob):
    sep("ElGamal - Déchiffrement (Ex2 Q3)")
    print("s = C1^b mod p")
    s = pow_mod_verbose(C1, b_bob, p)

    sep("Inverse de s modulo p")
    ok, s_inv = inv_mod(s, p, show=True)
    if not ok:
        print("ERREUR: s non inversible mod p (devrait être ok si p premier et s != 0).")
        return None

    sep("M = C2 * s^(-1) mod p")
    M = _mul_mod_verbose(C2, s_inv, p, label=None)

    sep("Résultat déchiffrement")
    print("M = {}".format(M))
    return M

def _elgamal_signature(M, p, g, a_alice, k):
    sep("ElGamal - Signature (Ex2 Q4/Q5)")
    print("On signe M = {}".format(M))
    print("Paramètres: p = {}, g = {}, a (priv Alice) = {}, k = {}".format(p, g, a_alice, k))
    pm1 = p - 1

    sep("Q4 - Inversibilité de k mod (p-1)")
    print("On travaille modulo p-1 = {}".format(pm1))
    ok, k_inv = inv_mod(k, pm1, show=True)
    if not ok:
        print("k n'est pas inversible modulo p-1 -> choisir un autre k.")
        return None, None, None

    sep("r = g^k mod p")
    r = pow_mod_verbose(g, k, p)

    sep("Calcul de (M - a*r) mod (p-1)")
    ar = (a_alice * r) % pm1
    val = (M - a_alice * r) % pm1
    print("a*r mod (p-1) = {}*{} mod {} = {}".format(a_alice, r, pm1, ar))
    print("(M - a*r) mod (p-1) = ({} - {}*{}) mod {} = {}".format(M, a_alice, r, pm1, val))

    sep("s = k^(-1) * (M - a*r) mod (p-1)")
    s_sig = (k_inv * val) % pm1
    print("k_inv = {}".format(k_inv))
    print("s = {} * {} mod {} = {}".format(k_inv, val, pm1, s_sig))

    sep("Signature (r, s)")
    print("(r, s) = ({}, {})".format(r, s_sig))
    return r, s_sig, k_inv

def _elgamal_verify_signature(M, p, g, a_alice, r, s_sig):
    sep("ElGamal - Vérification signature (Ex2 Q6)")
    print("Vérifier : g^M ?= y^r * r^s  [p]")

    sep("y = g^a mod p (clé publique Alice)")
    y = pow_mod_verbose(g, a_alice, p)

    sep("Gauche : g^M mod p")
    left = pow_mod_verbose(g, M, p)

    sep("Droite : y^r mod p")
    yr = pow_mod_verbose(y, r, p)

    sep("Droite : r^s mod p")
    rs = pow_mod_verbose(r, s_sig, p)

    sep("Produit : (y^r * r^s) mod p")
    right = _mul_mod_verbose(yr, rs, p, label=None)

    sep("Conclusion")
    if left == right:
        print("OK : {} == {} -> signature valide".format(left, right))
    else:
        print("NON : {} != {} -> signature invalide".format(left, right))

def ds_elgamal_ex2_run(choice):
    p = 23
    g = 5
    M = 10
    a = 3
    b = 6
    k = 7

    if choice in ("1", "5"):
        sep("Ex2 Q1 - Clé privée de Bob")
        print("b (clé privée de Bob) = {}".format(b))

    if choice in ("2", "5"):
        C1, C2, yB, s_shared = _elgamal_encrypt(M, p, g, a, b)

    if choice in ("3", "5"):
        C1, C2, yB, s_shared = _elgamal_encrypt(M, p, g, a, b)
        _elgamal_decrypt(C1, C2, p, b)

    if choice in ("4", "5"):
        r, s_sig, k_inv = _elgamal_signature(M, p, g, a, k)
        if r is not None:
            _elgamal_verify_signature(M, p, g, a, r, s_sig)

def elgamal_ds_menu():
    sep("DS - EXERCICE 2 (ElGamal)")
    print("1) Q1 (clé privée Bob)")
    print("2) Q2 (chiffrement C1,C2)")
    print("3) Q3 (déchiffrement)")
    print("4) Q4+Q5+Q6 (signature + vérif)")
    print("5) Tout l'exercice 2")
    print("6) Retour")
    ch = input("> Choix : ").strip()
    if ch in ("1", "2", "3", "4", "5"):
        ds_elgamal_ex2_run(ch)

def crypto_ds_menu():
    sep("MENU - DS CRYPTOGRAPHIE")
    print("1) Exercice 1 - RSA (valeurs du DS)")
    print("2) Exercice 2 - ElGamal (valeurs du DS)")
    print("3) Tout (Ex1 + Ex2)")
    print("4) Retour")
    ch = input("> Choix : ").strip()
    if ch == "1":
        rsa_ds_menu()
    elif ch == "2":
        elgamal_ds_menu()
    elif ch == "3":
        sep("RUN COMPLET - Ex1 RSA")
        ds_rsa_ex1_run("5")
        sep("RUN COMPLET - Ex2 ElGamal")
        ds_elgamal_ex2_run("5")

def menu():
    sep("MENU")
    print("1) Décomp. facteurs premiers")
    print("2) PGCD / Bézout")
    print("3) Inverse mod m")
    print("4) Équations modulaires")
    print("5) Tables (Z / Z_n)")
    print("6) CRT (théorème des restes chinois)")
    print("7) Puissance mod m")
    print("8) DS Cryptographie (RSA + ElGamal)")
    print("9) Quitter")
    choice = input("> Choix : ").strip()

    if choice == "1":
        show_factorization_and_option_gcd()
    elif choice == "2":
        run_pgcd_bezout()
    elif choice == "3":
        run_inverse()
    elif choice == "4":
        equations_menu_option()
    elif choice == "5":
        run_tables()
    elif choice == "6":
        solve_system_crt_coprime()
    elif choice == "7":
        run_pow_mod()
    elif choice == "8":
        crypto_ds_menu()
    elif choice == "9":
        print("Quitter le programme.")
        return
    else:
        print("Choix inconnu.")

menu()