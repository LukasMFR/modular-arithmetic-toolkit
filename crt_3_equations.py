def sep(title=None):
    if title:
        print("\n" + "-" * 10 + f" {title} " + "-" * 10)
    else:
        print("\n" + "-" * 38)

def gcd(a, b):
    a = abs(a); b = abs(b)
    while b:
        a, b = b, a % b
    return a

def egcd_verbose(a, b, show=True, show_back=True):
    A0, B0 = a, b
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    divs = []

    while r != 0:
        q = old_r // r
        rem = old_r - q * r
        divs.append((old_r, r, q, rem))
        old_r, r = r, rem
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t

    g, x, y = old_r, old_s, old_t

    if show:
        sep(f"Algorithme d'Euclide ({A0} , {B0})")
        for (A, B, q, r_) in divs:
            print(f"{A} = {q}*{B} + {r_}")
        print(f"pgcd({A0}, {B0}) = {g}")

    if show and show_back:
        sep("Résultat Bézout (coeffs)")
        print(f"x = {x}, y = {y}")
        print(f"Vérif : {A0}*{x} + {B0}*{y} = {A0*x + B0*y}")

    return g, x, y

def inv_mod_verbose(a, m):
    sep(f"Inverse modulaire : trouver {a}^(-1) [ {m} ]")
    if m <= 0:
        print("Erreur : m doit être > 0")
        return False, None
    g, x, _ = egcd_verbose(a, m, show=True, show_back=True)
    if g != 1:
        sep("Conclusion")
        print(f"pgcd({a}, {m}) = {g} ≠ 1 => pas d'inverse modulo {m}.")
        return False, None
    inv = x % m
    sep("Conclusion")
    print(f"{a}^(-1) ≡ {inv}  [ {m} ]")
    print(f"Vérif : ({a}*{inv}) % {m} = {(a*inv) % m}")
    return True, inv

def solve_crt_3_verbose(a1, m1, a2, m2, a3, m3):
    sep("Système CRT (3 équations) - ÉNONCÉ")
    a1 %= m1; a2 %= m2; a3 %= m3
    print(f"x ≡ {a1}  [ {m1} ]")
    print(f"x ≡ {a2}  [ {m2} ]")
    print(f"x ≡ {a3}  [ {m3} ]")

    sep("1) Vérification coprimalité (pairwise)")
    pairs = [("m1,m2", m1, m2), ("m1,m3", m1, m3), ("m2,m3", m2, m3)]
    ok = True
    for name, A, B in pairs:
        g = gcd(A, B)
        print(f"pgcd({name}) = pgcd({A},{B}) = {g}")
        if g != 1:
            ok = False

    if not ok:
        sep("Conclusion")
        print("Les modules ne sont PAS deux à deux copremiers => CRT (formule directe) non applicable ici.")
        print("Dans ton DS, si on te dit explicitement “théorème chinois (3 équations)”, en général ils sont copremiers.")
        return

    sep("2) Produit total M")
    M = m1 * m2 * m3
    print(f"M = m1*m2*m3 = {m1}*{m2}*{m3} = {M}")

    sep("3) Sous-produits Mi = M/mi")
    M1 = M // m1
    M2 = M // m2
    M3 = M // m3
    print(f"M1 = M/m1 = {M}/{m1} = {M1}")
    print(f"M2 = M/m2 = {M}/{m2} = {M2}")
    print(f"M3 = M/m3 = {M}/{m3} = {M3}")

    sep("4) Inverses yi : Mi*yi ≡ 1 [ mi ]")
    ok1, y1 = inv_mod_verbose(M1, m1)
    ok2, y2 = inv_mod_verbose(M2, m2)
    ok3, y3 = inv_mod_verbose(M3, m3)
    if not (ok1 and ok2 and ok3):
        sep("Erreur")
        print("Un inverse n'existe pas (ce qui ne devrait pas arriver si les mi sont copremiers).")
        return

    sep("5) Formule CRT")
    print("x0 ≡ a1*M1*y1 + a2*M2*y2 + a3*M3*y3  [ M ]")
    t1 = a1 * M1 * y1
    t2 = a2 * M2 * y2
    t3 = a3 * M3 * y3
    print(f"Terme1 = {a1}*{M1}*{y1} = {t1}")
    print(f"Terme2 = {a2}*{M2}*{y2} = {t2}")
    print(f"Terme3 = {a3}*{M3}*{y3} = {t3}")

    sep("6) Somme + réduction")
    S = t1 + t2 + t3
    print(f"S = {t1} + {t2} + {t3} = {S}")
    x0 = S % M
    print(f"x0 = S mod M = {S} mod {M} = {x0}")

    sep("7) Vérification")
    print(f"x0 mod m1 = {x0} mod {m1} = {x0 % m1} (attendu {a1})")
    print(f"x0 mod m2 = {x0} mod {m2} = {x0 % m2} (attendu {a2})")
    print(f"x0 mod m3 = {x0} mod {m3} = {x0 % m3} (attendu {a3})")

    sep("Conclusion")
    print(f"Solution canonique : x ≡ {x0}  [ {M} ]")
    print(f"Forme générale : x = {x0} + {M}*k,  k ∈ Z")

def main():
    sep("CHAPITRE 1 - Théorème chinois (3 congruences)")
    print("Tu vas entrer : x ≡ a1 [m1], x ≡ a2 [m2], x ≡ a3 [m3].")
    try:
        a1 = int(input("a1 = "))
        m1 = int(input("m1 (>0) = "))
        a2 = int(input("a2 = "))
        m2 = int(input("m2 (>0) = "))
        a3 = int(input("a3 = "))
        m3 = int(input("m3 (>0) = "))
        if m1 <= 0 or m2 <= 0 or m3 <= 0:
            print("Erreur : les modules doivent être > 0")
            return
    except:
        print("Entrée invalide.")
        return

    solve_crt_3_verbose(a1, m1, a2, m2, a3, m3)

main()
