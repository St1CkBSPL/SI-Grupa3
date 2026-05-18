def resolve(clause1, clause2):
    resolvents = []
    for lit1 in clause1:
        for lit2 in clause2:
            if lit1 == f"¬{lit2}" or lit2 == f"¬{lit1}":
                new_clause = list(clause1) + list(clause2)
                new_clause.remove(lit1) 
                new_clause.remove(lit2) 
                new_clause = list(set(new_clause)) 
                resolvents.append(new_clause)
    return resolvents

zdania_fol = [
    "∀x ((∀y (A(y) ⇒ L(x, y))) ⇒ ∃z L(z, x))", # 1. Każdy, kto kocha wszystkie zwierzęta, jest kochany
    "∀x (∃y (A(y) ∧ K(x, y)) ⇒ ∀z ¬L(z, x))", # 2. Nikt nie kocha tego, kto zabija zwierzę
    "∀x (A(x) ⇒ L(Jack, x))", # 3. Jack kocha wszystkie zwierzęta
    "K(Jack, Tuna) ∨ K(Jola, Tuna)", # 4. Jack lub Jola zabili Tunę
    "A(Tuna)", # 5. Tuna to zwierzę
    "¬K(Jola, Tuna)" # Zanegowany wniosek, zakładamy, że Jola nie zabiła Tuny
]


# Przykład konwersji Zdania 1 na postać CNF:
# Wejście: ∀x ((∀y (A(y) ⇒ L(x, y))) ⇒ ∃z L(z, x))
# 1. Eliminacja ⇒ : ∀x (¬(∀y (¬A(y) ∨ L(x, y))) ∨ ∃z L(z, x))
# 2. De Morgan    : ∀x (∃y (A(y) ∧ ¬L(x, y)) ∨ ∃z L(z, x))
# 3. Skolemizacja : ∀x ((A(F(x)) ∧ ¬L(x, F(x))) ∨ L(G(x), x))  # y -> F(x), z -> G(x)
# 4. Rozdzielność : (A(F(x)) ∨ L(G(x), x)) ∧ (¬L(x, F(x)) ∨ L(G(x), x))
# Wynik to dwie odrębne klauzule (K1 i K2).


# Reprezentacja bazy wiedzy w postaci klauzul (CNF)
klauzule_cnf = {
    "K1": ["A(F(Jack))", "L(G(Jack), Jack)"],                  # Z CNF Zdania 1
    "K2": ["¬L(Jack, F(Jack))", "L(G(Jack), Jack)"],         # Z CNF Zdania 1
    "K3": ["¬A(Tuna)", "¬K(Jack, Tuna)", "¬L(G(Jack), Jack)"], # Z CNF Zdania 2
    "K4": ["¬A(F(Jack))", "L(Jack, F(Jack))"],                 # Z CNF Zdania 3
    "K5": ["K(Jack, Tuna)", "K(Jola, Tuna)"],                  # Z CNF Zdania 4
    "K6": ["A(Tuna)"],                                         # Z CNF Zdania 5
    "K7": ["¬K(Jola, Tuna)"]                                   # Zanegowany wniosek
}

# Wykonanie dowodu metodą rezolucji
r1 = resolve(klauzule_cnf["K5"], klauzule_cnf["K7"])[0]
print(f"R1: {r1}") # Wynik: ['K(Jack, Tuna)']

r2 = resolve(klauzule_cnf["K3"], r1)[0]
print(f"R2: {r2}") # Wynik: ['¬L(G(Jack), Jack)', '¬A(Tuna)']

r3 = resolve(r2, klauzule_cnf["K6"])[0]
print(f"R3: {r3}") # Wynik: ['¬L(G(Jack), Jack)']

r4 = resolve(klauzule_cnf["K4"], klauzule_cnf["K2"])[0]
print(f"R4: {r4}") # Wynik: ['L(G(Jack), Jack)', '¬A(F(Jack))']

r5 = resolve(r4, klauzule_cnf["K1"])[0]
print(f"R5: {r5}") # Wynik: ['L(G(Jack), Jack)']

r6 = resolve(r3, r5)[0]
print(f"R6 (Pusta klauzula): {r6}") # Wynik: [] -> Udowodniono sprzeczność