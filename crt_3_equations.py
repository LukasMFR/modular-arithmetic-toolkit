def sep(title=None):
    if title:
        print(f"--- {title} ---")
    else:
        print("-" * 38)

def gcd(a, b):
    a = abs(a); b = abs(b)
    while b:
        a, b = b, a % b
    return a

def egcd(a, b):
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    return old_r, old_s, old_t

def inv_mod_quick(a, m):
    if m <= 0:
        return False, None
    g, x, _ = egcd(a, m)
    if g != 1:
        return False, None
    return True, x % m

def solve_crt_3_compact(a1, m1, a2, m2, a3, m3):
    a1 %= m1
    a2 %= m2
    a3 %= m3

    print("Système :")
    print(f"x ≡ {a1}  [ {m1} ]")
    print(f"x ≡ {a2}  [ {m2} ]")
    print(f"x ≡ {a3}  [ {m3} ]")

    if gcd(m1, m2) != 1 or gcd(m1, m3) != 1 or gcd(m2, m3) != 1:
        sep("Erreur")
        print("Modules NON copremiers deux à deux => la formule CRT directe ne s'applique pas.")
        print("Dans ce cas, il faut traiter le cas général (pas demandé ici).")
        return

    sep("Produit total")
    M = m1 * m2 * m3
    print(f"M = {m1} * {m2} * {m3} = {M}")

    sep("Sous-produits")
    M1 = M // m1
    M2 = M // m2
    M3 = M // m3
    print(f"M1 = M / m1 = {M1}")
    print(f"M2 = M / m2 = {M2}")
    print(f"M3 = M / m3 = {M3}")

    sep("Recherche des inverses (Mi * yi ≡ 1 [mi])")

    ok1, y1 = inv_mod_quick(M1, m1)
    ok2, y2 = inv_mod_quick(M2, m2)
    ok3, y3 = inv_mod_quick(M3, m3)

    if not (ok1 and ok2 and ok3):
        sep("Erreur")
        print("Impossible de trouver un inverse (ne devrait pas arriver si les mi sont copremiers).")
        return

    r1, r2, r3 = M1 % m1, M2 % m2, M3 % m3
    print(f"{M1}*y1 ≡ 1 [{m1}] -> {M1} ≡ {r1} [{m1}] -> y1 ≡ {y1} [{m1}] => y1 = {y1}")
    print(f"{M2}*y2 ≡ 1 [{m2}] -> {M2} ≡ {r2} [{m2}] -> y2 ≡ {y2} [{m2}] => y2 = {y2}")
    print(f"{M3}*y3 ≡ 1 [{m3}] -> {M3} ≡ {r3} [{m3}] -> y3 ≡ {y3} [{m3}] => y3 = {y3}")

    sep("Construction (formule CRT)")
    print(f"x ≡ {a1} * {M1} * {y1}  +  {a2} * {M2} * {y2}  +  {a3} * {M3} * {y3}  [ {M} ]")

    sep("Calcul des termes")
    t1 = a1 * M1 * y1
    t2 = a2 * M2 * y2
    t3 = a3 * M3 * y3
    print(f"Terme #1 = {a1}*{M1}*{y1} = {t1}")
    print(f"Terme #2 = {a2}*{M2}*{y2} = {t2}")
    print(f"Terme #3 = {a3}*{M3}*{y3} = {t3}")

    sep("Somme")
    S = t1 + t2 + t3
    print(f"S = {t1} + {t2} + {t3} = {S}")

    sep("Réduction")
    x0 = S % M
    print(f"x0 = {S} % {M} = {x0}")

    sep("Solution canonique")
    print(f"x ≡ {x0}  [ {M} ]")

    sep("Vérifications")
    checks = [(m1, a1), (m2, a2), (m3, a3)]
    for mi, ai in checks:
        val = x0 % mi
        ok = "  (ok)" if val == ai else "  (!!)"
        print(f"{x0} % {mi} = {val}  (attendu {ai}){ok}")

    sep("Forme générale")
    print(f"x = {x0} + {M}*k,  k entier")

def main():
    try:
        a1 = int(input("a1 = "))
        m1 = int(input("m1 (>0) = "))
        a2 = int(input("a2 = "))
        m2 = int(input("m2 (>0) = "))
        a3 = int(input("a3 = "))
        m3 = int(input("m3 (>0) = "))
        if m1 <= 0 or m2 <= 0 or m3 <= 0:
            print("Erreur : modules > 0 requis.")
            return
    except:
        print("Entrée invalide.")
        return

    solve_crt_3_compact(a1, m1, a2, m2, a3, m3)

    main()
