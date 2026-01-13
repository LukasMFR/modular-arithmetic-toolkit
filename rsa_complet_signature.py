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
        sep("Bézout (coeffs)")
        print(f"{g} = {x}*{A0} + {y}*{B0}")
        print(f"Vérif : {x}*{A0} + {y}*{B0} = {x*A0 + y*B0}")

    return g, x, y

def inv_mod_verbose(a, m):
    sep(f"Inverse modulaire : {a}^(-1) [ {m} ]")
    if m <= 0:
        print("Erreur : m doit être > 0")
        return False, None
    g, x, _ = egcd_verbose(a, m, show=True, show_back=True)
    if g != 1:
        sep("Conclusion")
        print(f"pgcd({a},{m}) = {g} ≠ 1 => pas d'inverse, donc pas de clé privée d.")
        return False, None
    inv = x % m
    sep("Conclusion")
    print(f"{a}^(-1) ≡ {inv}  [ {m} ]")
    print(f"Vérif : ({a}*{inv}) % {m} = {(a*inv) % m}")
    return True, inv

def pow_mod_verbose(a, e, m):
    sep('Puissance modulaire (décomposition binaire)')
    if m <= 0:
        print("Erreur : m doit être > 0")
        return None
    if e < 0:
        print("Erreur : exposant négatif non géré.")
        return None

    print(f"Objectif : calculer {a}^{e} mod {m}")
    a0, e0 = a, e

    # 1) Écriture binaire
    sep("1) Écriture de l'exposant en binaire")
    if e == 0:
        print("e = 0 => résultat = 1 mod m")
        return 1 % m

    bits = []
    t = e
    k = 0
    while t > 0:
        if t & 1:
            bits.append(k)
        t >>= 1
        k += 1
    bits_desc = sorted(bits, reverse=True)
    print(f"Bits à 1 : {', '.join('2^'+str(b) for b in bits_desc)}")
    print(f"Donc {e} = " + " + ".join(str(1 << b) for b in bits_desc))

    # 2) Paliers (carrés successifs)
    sep("2) Paliers : a^(2^k) mod m")
    a_mod = a % m
    pow_vals = {0: a_mod}
    print(f"a^(2^0) = a^1 ≡ {a_mod} [ {m} ]")
    max_k = bits_desc[0] if bits_desc else 0
    prev = a_mod
    for kk in range(1, max_k + 1):
        prev = (prev * prev) % m
        pow_vals[kk] = prev
        print(f"a^(2^{kk}) ≡ (a^(2^{kk-1}))^2 ≡ {prev} [ {m} ]")

    # 3) Assemblage
    sep("3) Assemblage des facteurs utiles")
    acc = 1 % m
    first = True
    for kk in bits_desc:
        if first:
            acc = pow_vals[kk]
            print(f"Start = a^(2^{kk}) ≡ {acc} [ {m} ]")
            first = False
        else:
            before = acc
            acc = (acc * pow_vals[kk]) % m
            print(f"acc = ({before} * {pow_vals[kk]}) mod {m} = {acc}")

    sep("Résultat")
    print(f"{a0}^{e0} mod {m} = {acc}")
    return acc

def pow_mod_fast(a, e, m):
    if m <= 0:
        return 0
    a %= m
    res = 1 % m
    while e > 0:
        if e & 1:
            res = (res * a) % m
        a = (a * a) % m
        e >>= 1
    return res

def rsa_keygen_verbose(p, q, e, who=""):
    sep(f"RSA - Génération de clés {who}".strip())
    print(f"p = {p}, q = {q}, e = {e}")
    n = p * q
    phi = (p - 1) * (q - 1)

    sep("1) Calcul n et φ(n)")
    print(f"n = p*q = {p}*{q} = {n}")
    print(f"φ(n) = (p-1)(q-1) = ({p}-1)({q}-1) = {phi}")

    sep("2) Vérifier pgcd(e, φ(n)) = 1")
    g = gcd(e, phi)
    print(f"pgcd({e}, {phi}) = {g}")
    if g != 1:
        sep("Conclusion")
        print("e n'est pas inversible modulo φ(n) => impossible de calculer d.")
        return None

    sep("3) Calcul d = e^(-1) mod φ(n) (étapes)")
    ok, d = inv_mod_verbose(e, phi)
    if not ok:
        return None

    sep("Clés")
    print(f"Clé publique  (n, e) = ({n}, {e})")
    print(f"Clé privée    (n, d) = ({n}, {d})")
    return (n, e, d, phi)

def rsa_encrypt_verbose(m, n, e):
    sep("RSA - Chiffrement")
    print("Formule : c = m^e mod n")
    print(f"m = {m}, e = {e}, n = {n}")
    c = pow_mod_verbose(m, e, n)
    return c

def rsa_decrypt_verbose(c, n, d):
    sep("RSA - Déchiffrement")
    print("Formule : m = c^d mod n")
    print(f"c = {c}, d = {d}, n = {n}")
    m = pow_mod_verbose(c, d, n)
    return m

def rsa_sign_verbose(m, nA, dA):
    sep("RSA - Signature (Alice)")
    print("Signature : s = m^dA mod nA")
    print(f"m = {m}, dA = {dA}, nA = {nA}")
    s = pow_mod_verbose(m, dA, nA)
    return s

def rsa_verify_verbose(m, s, nA, eA):
    sep("RSA - Vérification signature (Bob)")
    print("Vérif : v = s^eA mod nA ; signature valide si v == m mod nA")
    print(f"m = {m}, s = {s}, eA = {eA}, nA = {nA}")
    v = pow_mod_verbose(s, eA, nA)
    print(f"m mod nA = {m % nA}")
    print(f"v        = {v}")
    sep("Conclusion")
    if v == (m % nA):
        print("Signature VALIDE ✅")
        return True
    else:
        print("Signature INVALIDE ❌")
        return False

def main():
    sep("CHAPITRE 3 - RSA complet (jusqu’à signature)")
    print("On va générer les clés Alice et Bob avec (p,q,e).")
    print("Ensuite : chiffrement, signature, vérification.")
    print("\n⚠️ Rappel DS : il faut souvent m < n (et messages réduits mod n).")

    try:
        sep("Entrée paramètres ALICE")
        pA = int(input("pA = "))
        qA = int(input("qA = "))
        eA = int(input("eA = "))

        sep("Entrée paramètres BOB")
        pB = int(input("pB = "))
        qB = int(input("qB = "))
        eB = int(input("eB = "))

        m = int(input("\nMessage m = "))
    except:
        print("Entrée invalide.")
        return

    keyA = rsa_keygen_verbose(pA, qA, eA, who="(Alice)")
    if keyA is None:
        return
    nA, eA, dA, phiA = keyA

    keyB = rsa_keygen_verbose(pB, qB, eB, who="(Bob)")
    if keyB is None:
        return
    nB, eB, dB, phiB = keyB

    sep("MENU RSA")
    print("1) Chiffrer m pour Bob")
    print("2) Déchiffrer un c (pour Bob)")
    print("3) Signer m (Alice) + Vérifier (Bob)")
    print("4) Chiffrer pour Bob ET signer le chiffré (comme dans ton ancien code)")
    print("5) Signer puis chiffrer (m et la signature)")
    print("6) Tout (démo complète)")
    ch = input("> Choix : ").strip()

    if ch == "1":
        c = rsa_encrypt_verbose(m, nB, eB)
        sep("Résultat")
        print(f"c = {c}")

    elif ch == "2":
        try:
            c = int(input("c = "))
        except:
            print("Entrée invalide.")
            return
        m_back = rsa_decrypt_verbose(c, nB, dB)
        sep("Résultat")
        print(f"m = {m_back}")

    elif ch == "3":
        s = rsa_sign_verbose(m, nA, dA)
        rsa_verify_verbose(m, s, nA, eA)

    elif ch == "4":
        sep("Étape A) Bob : chiffrement de m")
        c = rsa_encrypt_verbose(m, nB, eB)

        sep("Étape B) Alice : signature du chiffré c")
        print("Ici on signe le chiffré : sigma = c^dA mod nA")
        sigma = pow_mod_verbose(c, dA, nA)

        sep("Résultats")
        print(f"c      = {c}")
        print(f"sigma  = {sigma}")

        sep("Réception : vérification de la signature sur c")
        print("Bob calcule v = sigma^eA mod nA, et compare à c mod nA")
        v = pow_mod_verbose(sigma, eA, nA)
        print(f"c mod nA = {c % nA}")
        print(f"v        = {v}")
        print("Conclusion :", "VALIDE ✅" if v == (c % nA) else "INVALIDE ❌")

        sep("Puis Bob déchiffre c -> m")
        m_back = rsa_decrypt_verbose(c, nB, dB)
        print(f"m reçu = {m_back}")

    elif ch == "5":
        sep("A) Alice signe le message : s = m^dA mod nA")
        s = rsa_sign_verbose(m, nA, dA)

        sep("B) Bob doit recevoir (m, s) de façon confidentielle : on chiffre séparément")
        print("On chiffre m et s avec la clé publique de Bob (nB,eB).")
        c_m = rsa_encrypt_verbose(m, nB, eB)
        c_s = rsa_encrypt_verbose(s, nB, eB)

        sep("C) Réception Bob : déchiffre puis vérifie")
        m_recv = rsa_decrypt_verbose(c_m, nB, dB)
        s_recv = rsa_decrypt_verbose(c_s, nB, dB)
        rsa_verify_verbose(m_recv, s_recv, nA, eA)

    elif ch == "6":
        sep("1) Chiffrement pour Bob")
        c = rsa_encrypt_verbose(m, nB, eB)
        print(f"c = {c}")

        sep("2) Déchiffrement par Bob")
        m_back = rsa_decrypt_verbose(c, nB, dB)
        print(f"m' = {m_back}")

        sep("3) Signature par Alice (sur m)")
        s = rsa_sign_verbose(m, nA, dA)
        print(f"s = {s}")

        sep("4) Vérification par Bob")
        rsa_verify_verbose(m, s, nA, eA)

    else:
        print("Choix inconnu.")

main()
