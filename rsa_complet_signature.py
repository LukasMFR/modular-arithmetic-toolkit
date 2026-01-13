def sep(title=None):
    if title:
        print("--- {} ---".format(title))
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

def inv_mod_compact(a, m):
    if m <= 0:
        return False, None
    g, x, _ = egcd(a, m)
    if g != 1:
        return False, None
    return True, x % m

def pow_mod_compact(a, e, m, show_steps=True, title=None):
    if title:
        sep(title)
    if m <= 0:
        print("Erreur : m doit être > 0")
        return None
    if e < 0:
        print("Erreur : exposant négatif non géré.")
        return None

    a0, e0 = a, e
    a %= m

    if not show_steps:
        res = 1 % m
        while e > 0:
            if e & 1:
                res = (res * a) % m
            a = (a * a) % m
            e >>= 1
        return res

    print("Objectif : {}^{} mod {}".format(a0, e0, m))

    if e0 == 0:
        print("e = 0 => résultat = 1 mod {}".format(m))
        sep("Résultat")
        print("{}^{} mod {} = {}".format(a0, e0, m, 1 % m))
        return 1 % m

    bits = []
    t = e0
    k = 0
    while t > 0:
        if t & 1:
            bits.append(k)
        t >>= 1
        k += 1
    bits_desc = sorted(bits, reverse=True)

    sep("1) Binaire")
    print("Bits à 1 :", ", ".join("2^{}".format(b) for b in bits_desc))
    print("{} = {}".format(e0, " + ".join(str(1 << b) for b in bits_desc)))

    sep("2) Paliers (carrés successifs)")
    pow_vals = {0: a % m}
    print("a^(2^0) ≡ {} [ {} ]".format(pow_vals[0], m))
    max_k = bits_desc[0] if bits_desc else 0
    prev = pow_vals[0]
    for kk in range(1, max_k + 1):
        prev = (prev * prev) % m
        pow_vals[kk] = prev
        print("a^(2^{}) ≡ {} [ {} ]".format(kk, prev, m))

    sep("3) Assemblage")
    acc = 1 % m
    first = True
    for kk in bits_desc:
        if first:
            acc = pow_vals[kk]
            print("Start = a^(2^{}) ≡ {} [ {} ]".format(kk, acc, m))
            first = False
        else:
            before = acc
            acc = (acc * pow_vals[kk]) % m
            print("acc = ({} * {}) mod {} = {}".format(before, pow_vals[kk], m, acc))

    sep("Résultat")
    print("{}^{} mod {} = {}".format(a0, e0, m, acc))
    return acc

def rsa_keygen_compact(p, q, e, who=""):
    label = "RSA - Génération de clés {}".format(who).strip()
    sep(label)
    print("p = {}, q = {}, e = {}".format(p, q, e))

    sep("1) Calcul n et φ(n)")
    n = p * q
    phi = (p - 1) * (q - 1)
    print("n = p*q = {}*{} = {}".format(p, q, n))
    print("φ(n) = (p-1)(q-1) = ({}-1)({}-1) = {}".format(p, q, phi))

    sep("2) Condition : pgcd(e, φ(n)) = 1")
    g = gcd(e, phi)
    print("pgcd({}, {}) = {}".format(e, phi, g))
    if g != 1:
        sep("Conclusion")
        print("e non inversible modulo φ(n) => impossible de calculer d.")
        return None

    sep("3) Calcul d = e^-1 mod φ(n)")
    ok, d = inv_mod_compact(e, phi)
    if not ok:
        sep("Conclusion")
        print("Impossible de calculer d (e non inversible).")
        return None
    print("d ≡ e^-1 [φ(n)] = {}^-1 [ {} ] = {}".format(e, phi, d))
    print("Vérif : ({}*{}) % {} = {}".format(e, d, phi, (e * d) % phi))

    sep("Clés")
    print("Clé publique (n, e) = ({}, {})".format(n, e))
    print("Clé privée   (n, d) = ({}, {})".format(n, d))
    return (n, e, d, phi)

def rsa_encrypt_compact(m, n, e):
    sep("RSA - Chiffrement")
    print("Formule : c = m^e mod n")
    print("m = {}, e = {}, n = {}".format(m, e, n))
    c = pow_mod_compact(m, e, n, show_steps=True, title="Puissance modulaire")
    sep("Résultat")
    print("c = {}".format(c))
    return c

def rsa_decrypt_compact(c, n, d):
    sep("RSA - Déchiffrement")
    print("Formule : m = c^d mod n")
    print("c = {}, d = {}, n = {}".format(c, d, n))
    m = pow_mod_compact(c, d, n, show_steps=True, title="Puissance modulaire")
    sep("Résultat")
    print("m = {}".format(m))
    return m

def rsa_sign_message_compact(m, nA, dA):
    sep("RSA - Signature (sur m)")
    print("Signature : s = m^dA mod nA")
    print("m = {}, dA = {}, nA = {}".format(m, dA, nA))
    s = pow_mod_compact(m, dA, nA, show_steps=True, title="Puissance modulaire")
    sep("Résultat")
    print("s = {}".format(s))
    return s

def rsa_verify_message_compact(m, s, nA, eA):
    sep("RSA - Vérification signature (sur m)")
    print("Calcul : v = s^eA mod nA")
    print("Signature valide si v == m mod nA")
    print("m = {}, s = {}, eA = {}, nA = {}".format(m, s, eA, nA))
    v = pow_mod_compact(s, eA, nA, show_steps=True, title="Puissance modulaire")
    mm = m % nA
    sep("Comparaison")
    print("m mod nA = {}".format(mm))
    print("v        = {}".format(v))
    sep("Conclusion")
    if v == mm:
        print("Signature VALIDE")
        return True
    else:
        print("Signature INVALIDE")
        return False

def rsa_sign_cipher_compact(c, nA, dA):
    sep("RSA - Signature (sur c)")
    print("Signature : sigma = c^dA mod nA")
    print("c = {}, dA = {}, nA = {}".format(c, dA, nA))
    sigma = pow_mod_compact(c, dA, nA, show_steps=True, title="Puissance modulaire")
    sep("Résultat")
    print("sigma = {}".format(sigma))
    return sigma

def rsa_verify_cipher_compact(c, sigma, nA, eA):
    sep("RSA - Vérification signature (sur c)")
    print("Calcul : v = sigma^eA mod nA")
    print("Signature valide si v == c mod nA")
    print("c = {}, sigma = {}, eA = {}, nA = {}".format(c, sigma, eA, nA))
    v = pow_mod_compact(sigma, eA, nA, show_steps=True, title="Puissance modulaire")
    cc = c % nA
    sep("Comparaison")
    print("c mod nA = {}".format(cc))
    print("v        = {}".format(v))
    sep("Conclusion")
    if v == cc:
        print("Signature VALIDE")
        return True
    else:
        print("Signature INVALIDE")
        return False

def main():
    sep("RSA complet (compact) : chiffrement + signature")
    print("Paramètres : p, q, e pour Alice et Bob.")
    print("Ensuite : calcul des clés, chiffrement, signature, vérification.")

    try:
        sep("Entrée paramètres ALICE")
        pA = int(input("pA = "))
        qA = int(input("qA = "))
        eA = int(input("eA = "))

        sep("Entrée paramètres BOB")
        pB = int(input("pB = "))
        qB = int(input("qB = "))
        eB = int(input("eB = "))
    except:
        print("Entrée invalide.")
        return

    keyA = rsa_keygen_compact(pA, qA, eA, who="(Alice)")
    if keyA is None:
        return
    nA, eA, dA, phiA = keyA

    keyB = rsa_keygen_compact(pB, qB, eB, who="(Bob)")
    if keyB is None:
        return
    nB, eB, dB, phiB = keyB

    sep("MENU")
    print("1) Chiffrer un message M pour Bob (confidentialité)")
    print("2) Déchiffrer un message C avec la clé privée de Bob")
    print("3) Signer un message m (Alice) et vérifier (Bob) (authenticité)")
    print("4) Chiffrer m pour Bob puis signer le chiffré C(m) (cas classique : confidentiel + authentique)")
    print("5) Démo complète : (4) + déchiffrement + vérification")
    ch = input("> Choix : ").strip()

    if ch == "1":
        try:
            M = int(input("Message M = "))
        except:
            print("Entrée invalide.")
            return
        rsa_encrypt_compact(M, nB, eB)

    elif ch == "2":
        try:
            C = int(input("Chiffré C = "))
        except:
            print("Entrée invalide.")
            return
        rsa_decrypt_compact(C, nB, dB)

    elif ch == "3":
        try:
            m = int(input("Message m = "))
        except:
            print("Entrée invalide.")
            return
        s = rsa_sign_message_compact(m, nA, dA)
        rsa_verify_message_compact(m, s, nA, eA)

    elif ch == "4":
        try:
            m = int(input("Message m = "))
        except:
            print("Entrée invalide.")
            return

        sep("A) Confidentialité : Bob chiffre/définit C(m)")
        c = rsa_encrypt_compact(m, nB, eB)

        sep("B) Authenticité : Alice signe le chiffré")
        sigma = rsa_sign_cipher_compact(c, nA, dA)

        sep("Résultats à envoyer à Bob")
        print("C(m)  = {}".format(c))
        print("sigma = {}".format(sigma))

        sep("Réception Bob : vérifier la signature sur C(m)")
        rsa_verify_cipher_compact(c, sigma, nA, eA)

    elif ch == "5":
        try:
            m = int(input("Message m = "))
        except:
            print("Entrée invalide.")
            return

        sep("A) Chiffrement pour Bob")
        c = rsa_encrypt_compact(m, nB, eB)

        sep("B) Signature (sur C(m)) par Alice")
        sigma = rsa_sign_cipher_compact(c, nA, dA)

        sep("C) Vérification signature par Bob")
        ok = rsa_verify_cipher_compact(c, sigma, nA, eA)

        sep("D) Déchiffrement par Bob")
        m_back = rsa_decrypt_compact(c, nB, dB)

        sep("Conclusion finale")
        print("Message déchiffré m' = {}".format(m_back))
        print("Signature (sur C(m)) :", "VALIDE" if ok else "INVALIDE")

    else:
        print("Choix inconnu.")

main()
