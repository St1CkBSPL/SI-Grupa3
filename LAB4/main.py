# =====================================================================
# ZADANIE 1: Funkcja PL-TRUE (Ewaluacja rekurencyjna zdania logicznego)
# =====================================================================

def PL_TRUE(S, m):
    """
    Sprawdza, czy zdanie S jest prawdziwe dla przypisania m.
    S - zdanie (np. krotka: ('AND', 'A', 'B') lub pojedynczy symbol 'A')
    m - słownik przypisań (np. {'A': 0, 'B': 1})
    """
    # Baza rekurencji: jeśli S jest pojedynczym symbolem (zmienną)
    if isinstance(S, str):
        return bool(m.get(S, False))

    # Baza rekurencji: jeśli S jest od razu wartością logiczną
    if isinstance(S, bool):
        return S

    # Krok rekurencyjny: interpretacja spójników
    operator = S[0]

    if operator == 'NOT':
        return not PL_TRUE(S[1], m)
    elif operator == 'AND':
        return PL_TRUE(S[1], m) and PL_TRUE(S[2], m)
    elif operator == 'OR':
        return PL_TRUE(S[1], m) or PL_TRUE(S[2], m)
    elif operator == 'IMPLIES':
        return (not PL_TRUE(S[1], m)) or PL_TRUE(S[2], m)
    elif operator == 'IFF':
        return PL_TRUE(S[1], m) == PL_TRUE(S[2], m)
    else:
        raise ValueError(f"Nieznany spójnik: {operator}")


# =====================================================================
# ZADANIE 2 (iii): Reguła Rezolucji (PL-RESOLUTION)
# =====================================================================

def pl_resolve(ci, cj):
    """
    Zwraca zbiór rezolwentów (nowych klauzul) z dwóch podanych klauzul.
    """
    resolvents = set()
    for literal in ci:
        # Znalezienie literału uzupełniającego
        comp = literal[1:] if literal.startswith('-') else '-' + literal

        if comp in cj:
            # Łączymy klauzule i usuwamy parę uzupełniającą się
            new_clause = set(ci) | set(cj)
            new_clause.remove(literal)
            new_clause.remove(comp)

            # Eliminacja tautologii (np. zawiera A i -A)
            is_tautology = False
            for l in new_clause:
                comp_l = l[1:] if l.startswith('-') else '-' + l
                if comp_l in new_clause:
                    is_tautology = True
                    break

            if not is_tautology:
                resolvents.add(frozenset(new_clause))
    return resolvents


def pl_resolution(kb_clauses, alpha_neg_clauses):
    """
    Sprawdza, czy KB dowodzi alpha za pomocą algorytmu rezolucji.
    """
    clauses = kb_clauses.union(alpha_neg_clauses)
    new = set()

    while True:
        clauses_list = list(clauses)
        n = len(clauses_list)

        for i in range(n):
            for j in range(i + 1, n):
                ci = clauses_list[i]
                cj = clauses_list[j]

                resolvents = pl_resolve(ci, cj)

                # Pusta klauzula oznacza sprzeczność (sukces dowodu nie wprost)
                if frozenset() in resolvents:
                    return True

                new.update(resolvents)

        # Jeśli nie możemy wygenerować nic nowego, dowód się nie powiódł
        if new.issubset(clauses):
            return False

        clauses.update(new)


# =====================================================================
# BLOK TESTOWY WIDOCZNY PO URUCHOMIENIU SKRYPTU
# =====================================================================

if __name__ == "__main__":
    print("=" * 50)
    print("WYNIKI DZIAŁANIA PROGRAMU")
    print("=" * 50)

    # --- Test Zadania 1 ---
    print("\n[ZADANIE 1] Ewaluacja rekurencyjna (PL-TRUE):")
    # S = ~A AND B
    S_przyklad = ('AND', ('NOT', 'A'), 'B')
    m_przyklad = {'A': 0, 'B': 1}
    wynik_zad1 = PL_TRUE(S_przyklad, m_przyklad)

    print(f"Zdanie logiczne S: {S_przyklad}")
    print(f"Model (przypisanie) m: {m_przyklad}")
    print(f"Czy zdanie S jest prawdziwe w modelu m? -> {wynik_zad1}")

    # --- Zadanie 2 (i) ---
    print("\n[ZADANIE 2 (i)] Teoretyczna liczba sytuacji:")
    liczba_sytuacji = 8 * 4  # 8 (doły) * 4 (Wumpus)
    print(f"Zgodnie z poleceniem i slajdami, łączna liczba rozważanych sytuacji to: {liczba_sytuacji}")

    # --- Test Zadania 2 (iii) ---
    print("\n[ZADANIE 2 (iii)] Algorytm Rezolucji ze Świata Wumpusa:")
    # Baza Wiedzy (KB) ze slajdu 22 (SI-W8) w formie CNF
    kb_wumpus = {
        frozenset({'-P21', 'B11'}),
        frozenset({'-B11', 'P12', 'P21'}),
        frozenset({'-P12', 'B11'}),
        frozenset({'-B11'})
    }

    # Cel: Udowodnić ~P1,2.
    # W dowodzie przez rezolucję dołączamy NEGACJĘ celu do KB.
    # ~(~P1,2) -> P1,2
    negacja_celu = {frozenset({'P12'})}

    wynik_zad2 = pl_resolution(kb_wumpus, negacja_celu)

    print("Baza wiedzy (KB): zdefiniowana zgodnie ze slajdem 22.")
    print("Szukany cel (alpha): ~P1,2 (w polu [1,2] nie ma dołu).")
    print(f"Czy KB dowodzi alpha (według algorytmu PL-RESOLUTION)? -> {wynik_zad2}")
    print("=" * 50)