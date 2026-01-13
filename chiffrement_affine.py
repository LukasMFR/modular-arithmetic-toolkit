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

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
M = 26

def char_to_int(c):
    return ALPHABET.index(c)

def int_to_char(x):
    return ALPHABET[x % M]

def normalize_text(s):
    return s.upper()

def affine_encrypt_compact(plain, a, b):
    sep("Chiffrement affine")
    print("E(x) = (a*x + b) mod 26")
    print("a = {}, b = {}".format(a, b))

    sep("Condition")
    g = gcd(a, M)
    print("pgcd({}, 26) = {}".format(a, g))
    if g != 1:
        print("a non inversible modulo 26 => impossible.")
        return None

    plain = normalize_text(plain)
    sep("Calcul (lettres uniquement)")
    out = []
    for ch in plain:
        if ch in ALPHABET:
            x = char_to_int(ch)
            y = (a * x + b) % M
            print("{}({}) -> ({}*{}+{}) mod 26 = {} -> {}".format(
                ch, x, a, x, b, y, int_to_char(y)
            ))
            out.append(int_to_char(y))
        else:
            out.append(ch)

    cipher = "".join(out)
    sep("Résultat")
    print("Texte chiffré = {}".format(cipher))
    return cipher

def invert_affine_function_compact(a, b):
    sep("Inverser la fonction affine")
    print("f(x) = a*x + b  [26]")
    print("a = {}, b = {}".format(a, b))

    sep("Condition")
    g = gcd(a, M)
    print("pgcd({}, 26) = {}".format(a, g))
    if g != 1:
        print("a non inversible modulo 26 => pas d'inverse de f.")
        return None

    sep("1) Inverse de a (mod 26)")
    ok, ainv = inv_mod_compact(a, M)
    if not ok:
        print("Impossible (ne devrait pas arriver si pgcd(a,26)=1).")
        return None
    print("a^-1 ≡ {}  [26]".format(ainv))
    print("Vérif : ({}*{}) % 26 = {}".format(a, ainv, (a*ainv) % 26))

    sep("2) Dérivation de f^-1")
    print("y ≡ a*x + b  [26]")
    print("y - b ≡ a*x  [26]")
    print("x ≡ a^-1*(y - b)  [26]")
    print("x ≡ a^-1*y - a^-1*b  [26]")

    sep("3) Mise sous forme (A*y + B) [26]")
    A = ainv % M
    B = (-ainv * b) % M
    print("A = a^-1 mod 26 = {}".format(A))
    print("B = (-a^-1*b) mod 26 = (-{}*{}) mod 26 = {}".format(ainv, b, B))
    print("Donc f^-1(y) = {}*y + {}  [26]".format(A, B))

    sep("Mini-vérif symbolique")
    print("Si x = f^-1(y), alors f(x) = y (mod 26).")
    print("Tu peux tester une valeur avec l'option table si besoin.")

    rep = input("Afficher la table (y->x) pour A..Z ? (o/n) : ").strip().lower()
    if rep == "o" or rep == "oui":
        sep("Table (y -> x)")
        print("y  -> x")
        for y in range(26):
            x = (A * y + B) % 26
            print("{}({}) -> {}({})".format(int_to_char(y), y, int_to_char(x), x))

    return A, B

def find_a_b_from_two_pairs_compact(p1, c1, p2, c2):
    sep("Retrouver (a,b) avec 2 paires")
    print("c ≡ a*p + b  [26]")

    p1 = p1.upper(); c1 = c1.upper()
    p2 = p2.upper(); c2 = c2.upper()

    if p1 not in ALPHABET or c1 not in ALPHABET or p2 not in ALPHABET or c2 not in ALPHABET:
        print("Erreur : lettres A..Z uniquement.")
        return None

    P1 = char_to_int(p1); C1 = char_to_int(c1)
    P2 = char_to_int(p2); C2 = char_to_int(c2)

    sep("1) Soustraction (éliminer b)")
    dC = (C1 - C2) % M
    dP = (P1 - P2) % M
    print("{}({}) ≡ a*{}({}) + b [26]".format(c1, C1, p1, P1))
    print("{}({}) ≡ a*{}({}) + b [26]".format(c2, C2, p2, P2))
    print("ΔC = ({}-{}) mod 26 = {}".format(C1, C2, dC))
    print("ΔP = ({}-{}) mod 26 = {}".format(P1, P2, dP))
    print("=> a*{} ≡ {} [26]".format(dP, dC))

    sep("2) Inverse de ΔP (mod 26)")
    ok, inv_dP = inv_mod_compact(dP, M)
    if not ok:
        print("ΔP non inversible mod 26 => pas de solution unique.")
        return None
    print("(ΔP)^-1 ≡ {} [26]".format(inv_dP))

    sep("3) Calcul de a puis b")
    a = (dC * inv_dP) % M
    b = (C1 - a * P1) % M
    print("a = {}*{} mod 26 = {}".format(dC, inv_dP, a))
    print("b = {} - {}*{} mod 26 = {}".format(C1, a, P1, b))

    sep("Conclusion")
    print("a = {}, b = {}".format(a, b))
    print("Vérif : (a*P1+b) mod 26 = {} (attendu {})".format((a*P1+b) % 26, C1))
    print("Vérif : (a*P2+b) mod 26 = {} (attendu {})".format((a*P2+b) % 26, C2))
    return a, b

def main():
    sep("Chiffrement affine (compact)")
    print("1) Chiffrer")
    print("2) Inverser la fonction f(x)=a*x+b [26]")
    print("3) Retrouver (a,b) avec 2 correspondances")
    ch = input("> Choix : ").strip()

    if ch == "1":
        try:
            a = int(input("a = "))
            b = int(input("b = "))
            plain = input("Texte à chiffrer = ")
        except:
            print("Entrée invalide.")
            return
        affine_encrypt_compact(plain, a, b)

    elif ch == "2":
        try:
            a = int(input("a = "))
            b = int(input("b = "))
        except:
            print("Entrée invalide.")
            return
        invert_affine_function_compact(a, b)

    elif ch == "3":
        print("Deux correspondances (lettre -> lettre).")
        p1 = input("Plain #1 = ").strip()
        c1 = input("Cipher #1 = ").strip()
        p2 = input("Plain #2 = ").strip()
        c2 = input("Cipher #2 = ").strip()
        find_a_b_from_two_pairs_compact(p1, c1, p2, c2)

    else:
        print("Choix inconnu.")

main()
