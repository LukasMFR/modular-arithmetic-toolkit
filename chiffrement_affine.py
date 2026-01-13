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

def egcd_verbose(a, b, show=True):
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
        sep(f"Euclide étendu ({A0}, {B0})")
        for (A, B, q, r_) in divs:
            print(f"{A} = {q}*{B} + {r_}")
        print(f"pgcd({A0},{B0}) = {g}")
        print(f"Bézout : {g} = {x}*{A0} + {y}*{B0}")
        print(f"Vérif : {x}*{A0} + {y}*{B0} = {x*A0 + y*B0}")

    return g, x, y

def inv_mod_verbose(a, m):
    sep(f"Inverse modulaire : {a}^(-1) [ {m} ]")
    if m <= 0:
        print("Erreur : m doit être > 0")
        return False, None
    g, x, _ = egcd_verbose(a, m, show=True)
    if g != 1:
        sep("Conclusion")
        print(f"pgcd({a},{m}) = {g} ≠ 1 => pas d'inverse.")
        return False, None
    inv = x % m
    sep("Conclusion")
    print(f"{a}^(-1) ≡ {inv}  [ {m} ]")
    print(f"Vérif : ({a}*{inv}) % {m} = {(a*inv) % m}")
    return True, inv

# --- Affine cipher helpers (alphabet A..Z -> 0..25)
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
M = 26

def char_to_int(c):
    return ALPHABET.index(c)

def int_to_char(x):
    return ALPHABET[x % M]

def normalize_text(s):
    # Met en majuscules, conserve espaces/ponctuation.
    return s.upper()

def affine_encrypt_verbose(plain, a, b):
    sep("Chiffrement affine - Rappel formule")
    print("E(x) = (a*x + b) mod 26")
    print(f"a = {a}, b = {b}, modulo = 26")

    sep("Vérification de la condition (a inversible mod 26)")
    g = gcd(a, M)
    print(f"pgcd({a}, 26) = {g}")
    if g != 1:
        print("=> a n'est PAS inversible modulo 26 => chiffrement affine impossible avec ce a.")
        return None

    plain = normalize_text(plain)
    sep("Conversion + calcul lettre par lettre")
    out = []
    for ch in plain:
        if ch in ALPHABET:
            x = char_to_int(ch)
            y = (a * x + b) % M
            print(f"{ch} -> x={x} ; y=(a*x+b) mod 26 = ({a}*{x}+{b}) mod 26 = {y} -> {int_to_char(y)}")
            out.append(int_to_char(y))
        else:
            out.append(ch)

    cipher = "".join(out)
    sep("Résultat")
    print(f"Texte chiffré = {cipher}")
    return cipher

def affine_decrypt_verbose(cipher, a, b):
    sep("Déchiffrement affine - Rappel formule")
    print("D(y) = a^{-1} * (y - b) mod 26")
    print(f"a = {a}, b = {b}, modulo = 26")

    sep("1) Calcul de a^{-1} mod 26")
    ok, ainv = inv_mod_verbose(a, M)
    if not ok:
        print("=> Déchiffrement impossible (a non inversible).")
        return None

    cipher = normalize_text(cipher)
    sep("2) Conversion + calcul lettre par lettre")
    out = []
    for ch in cipher:
        if ch in ALPHABET:
            y = char_to_int(ch)
            x = (ainv * ((y - b) % M)) % M
            print(f"{ch} -> y={y} ; x=a^-1*(y-b) mod 26 = {ainv}*({y}-{b}) mod 26 = {x} -> {int_to_char(x)}")
            out.append(int_to_char(x))
        else:
            out.append(ch)

    plain = "".join(out)
    sep("Résultat")
    print(f"Texte déchiffré = {plain}")
    return plain

def find_a_b_from_two_pairs_verbose(p1, c1, p2, c2):
    """
    Avec deux correspondances:
      c1 ≡ a*p1 + b [26]
      c2 ≡ a*p2 + b [26]
    => (c1 - c2) ≡ a*(p1 - p2) [26]
    """
    sep("Retrouver (a,b) à partir de 2 correspondances")
    print("Hypothèse : alphabet A..Z -> 0..25")
    print("c ≡ a*p + b [26]")

    p1 = p1.upper(); c1 = c1.upper(); p2 = p2.upper(); c2 = c2.upper()
    if p1 not in ALPHABET or c1 not in ALPHABET or p2 not in ALPHABET or c2 not in ALPHABET:
        print("Erreur : il faut donner des LETTRES A..Z.")
        return

    P1 = char_to_int(p1); C1 = char_to_int(c1)
    P2 = char_to_int(p2); C2 = char_to_int(c2)

    sep("1) Mise en équation")
    print(f"{c1}({C1}) ≡ a*{p1}({P1}) + b [26]")
    print(f"{c2}({C2}) ≡ a*{p2}({P2}) + b [26]")

    sep("2) Soustraction pour éliminer b")
    left = (C1 - C2) % M
    right_coeff = (P1 - P2) % M
    print(f"(C1 - C2) mod 26 = ({C1}-{C2}) mod 26 = {left}")
    print(f"(P1 - P2) mod 26 = ({P1}-{P2}) mod 26 = {right_coeff}")
    print(f"=> {left} ≡ a*{right_coeff}  [26]")

    sep("3) Résolution a*ΔP ≡ ΔC [26] (inverse de ΔP si possible)")
    ok, inv_dp = inv_mod_verbose(right_coeff, M)
    if not ok:
        print("ΔP n'est pas inversible mod 26 => ambigu / pas unique avec ces deux paires.")
        return

    a = (left * inv_dp) % M
    sep("4) Trouver b")
    # b ≡ C1 - a*P1 [26]
    b = (C1 - a * P1) % M
    print(f"a = ΔC * (ΔP)^-1 mod 26 = {left}*{inv_dp} mod 26 = {a}")
    print(f"b = C1 - a*P1 mod 26 = {C1} - {a}*{P1} mod 26 = {b}")

    sep("Conclusion")
    print(f"Paramètres trouvés : a = {a}, b = {b}")
    print("Vérif rapide :")
    print(f"  a*P1+b mod 26 = ({a}*{P1}+{b}) mod 26 = {(a*P1+b)%M} (attendu {C1})")
    print(f"  a*P2+b mod 26 = ({a}*{P2}+{b}) mod 26 = {(a*P2+b)%M} (attendu {C2})")

def main():
    sep("CHAPITRE 2 - Chiffrement affine")
    print("Alphabet : A..Z => 0..25 (mod 26).")
    print("1) Chiffrer")
    print("2) Déchiffrer")
    print("3) Retrouver (a,b) avec 2 correspondances (option utile en exo)")
    ch = input("> Choix : ").strip()

    if ch == "1":
        try:
            a = int(input("a = "))
            b = int(input("b = "))
            plain = input("Texte à chiffrer = ")
        except:
            print("Entrée invalide.")
            return
        affine_encrypt_verbose(plain, a, b)

    elif ch == "2":
        try:
            a = int(input("a = "))
            b = int(input("b = "))
            cipher = input("Texte à déchiffrer = ")
        except:
            print("Entrée invalide.")
            return
        affine_decrypt_verbose(cipher, a, b)

    elif ch == "3":
        print("Donne 2 correspondances (plaintext->ciphertext), une lettre à chaque fois.")
        p1 = input("Plain #1 (lettre) = ").strip()
        c1 = input("Cipher #1 (lettre) = ").strip()
        p2 = input("Plain #2 (lettre) = ").strip()
        c2 = input("Cipher #2 (lettre) = ").strip()
        find_a_b_from_two_pairs_verbose(p1, c1, p2, c2)

    else:
        print("Choix inconnu.")

main()
