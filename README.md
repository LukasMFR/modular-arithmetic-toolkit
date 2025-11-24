# Bézout, inverse modulaire et congruences (calculatrice Python)

Programme Python complet et optimisé pour **calculatrice Python**, dédié à l’étude des **équations et systèmes modulaires** en arithmétique.  
Ce script permet de manipuler les congruences, le PGCD, les inverses modulaires, les puissances mod m, ainsi que le théorème des restes chinois (CRT).

> 🧮 Version : **menu “one-shot”** — sans boucle continue, optimisée pour les environnements Python à mémoire limitée.

---

## 📚 Sommaire
1. [Présentation](#-présentation)
2. [Fonctionnalités](#-fonctionnalités)
3. [Structure du menu](#-structure-du-menu)
4. [Méthodes utilisées](#-méthodes-utilisées)
5. [Compatibilité](#-compatibilité)
6. [Exemples d’utilisation](#-exemples-dutilisation)
7. [Auteur](#-auteur)

---

## 🧩 Présentation

Ce programme regroupe dans un même fichier Python plusieurs outils de base en **arithmétique modulaire** :

- Calcul du **PGCD et des coefficients de Bézout**
- Recherche d’**inverses modulaires**
- Résolution d’**équations linéaires modulaires**
- Génération de **tables en Z et Zₙ**
- Application du **théorème des restes chinois (CRT)** pour des systèmes à modules copremiers
- Calcul de **puissances modulo m**  
  **→ avec réduction automatique de l’exposant par le théorème de Fermat lorsque m est premier**
- **Décomposition en facteurs premiers** (méthode de l’échelle)

Le script est conçu pour être **auto-suffisant**, pédagogique, et fonctionner sans dépendance externe.

---

## ⚙️ Fonctionnalités

| # | Fonction | Description | Exemple d’utilisation |
|---|-----------|--------------|------------------------|
| 1 | **Décomposition en facteurs premiers** | Factorise un entier et affiche les étapes de division. | `336 → 2⁴ × 3 × 7` |
| 2 | **PGCD / Bézout** | Applique l’algorithme d’Euclide étendu et montre la remontée pas à pas. | `pgcd(252, 198)` |
| 3 | **Inverse mod m** | Calcule et vérifie l’inverse modulaire si gcd(a, m) = 1. | `a = 7, m = 26 → 15` |
| 4 | **Équations modulaires** | Résout `a x ≡ b [m]`, `a x + c ≡ b [m]`, `x + c ≡ b [m]` avec mise en forme automatique. | `4x + 5 ≡ 0 [21]` |
| 5 | **Tables Z / Zₙ** | Affiche la table d’addition ou de multiplication sur un intervalle ou modulo n. | `Z₇* = {1,2,3,4,5,6}` |
| 6 | **CRT (formule directe)** | Résout un système de congruences copremières avec la formule du théorème des restes chinois. | `x ≡ 7 [10], x ≡ 3 [7], x ≡ 6 [13] → x ≡ 227 [910]` |
| 7 | **Puissance mod m** | Calcule `a^e mod m` étape par étape (décomposition binaire) **avec réduction Fermat si applicable**. | `3¹³ mod 17` |

---

## 🧮 Structure du menu

Lors de l’exécution, le programme affiche :

```

--- MENU ---

1. Décomp. facteurs premiers
2. PGCD / Bézout
3. Inverse mod m
4. Équations modulaires
5. Tables (Z / Z_n)
6. CRT (formule directe)
7. Puissance mod m
8. Quitter

```

Chaque option exécute une fonction spécifique.  
Le script ne relance pas le menu après une opération (version “one-shot”), ce qui permet d’économiser de la mémoire dans les environnements limités.

---

## 🧠 Méthodes utilisées

- **Algorithme d’Euclide étendu** pour le PGCD et les coefficients de Bézout.
- **Résolution d’équations modulaires** via l’inverse modulaire.
- **Théorème des restes chinois (CRT)** pour les systèmes à modules copremiers :
  \[
  x ≡ a_i \pmod{m_i}, \quad \text{avec } \gcd(m_i, m_j) = 1
  \]
  et construction :
  \[
  x ≡ \sum a_i M_i y_i \pmod{M}
  \]
- **Méthode de décomposition binaire** pour le calcul de puissances.
- **Théorème de Fermat** ajouté dans l’option 7 :  
  si `m` est premier et `gcd(a,m)=1`  
  \[
  a^{m-1} ≡ 1 \pmod{m}
  \]
  donc  
  \[
  a^e ≡ a^{\,e \bmod (m-1)} \pmod{m}
  \]

---

## 🧩 Compatibilité

* ✅ Compatible **Python standard**, MicroPython et environnements embarqués
* ⚙️ Taille max recommandée : **~30 Ko**
* ⚠️ Version *one-shot* : pas de boucle infinie (gain mémoire)

---

## 🔢 Exemple d’utilisation : CRT

```
> Choix : 6
--- CRT (formule directe) ---
Nombre d'équations k = 3
Equation #1 :
  a1 = 7
  m1 (>0) = 10
Equation #2 :
  a2 = 3
  m2 (>0) = 7
Equation #3 :
  a3 = 6
  m3 (>0) = 13
--- Produit total ---
M = 10 * 7 * 13 = 910
--- Inverses ---
y1 = 1, y2 = 2, y3 = 8
--- Construction ---
x ≡ 7*91*1 + 3*130*2 + 6*70*8 [910]
x0 = 227
✅ Résultat : x ≡ 227 [910]
```

---

## 👨‍💻 Auteur

**Lukas Mauffré**  
Étudiant à l’ECE Paris — Passionné de mathématiques, d’algorithmique et de NumWorks.  
Version : *menu “one-shot”, allégée pour NumWorks (RAM 32 Ko)*

---

> 💡 *Dernière mise à jour : novembre 2025*
