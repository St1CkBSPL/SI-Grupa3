##Zadanie 1

def mrv(variables, domains, assignment):
    # Wybieramy tylko te zmienne, które nie zostały jeszcze przypisane
    unassigned = [v for v in variables if v not in assignment]
    
    # 1.2 Zasada MRV: Zwracamy zmienną z najmniejszą liczbą dostępnych wartości w dziedzinie
    return min(unassigned, key=lambda v: len(domains[v]))

def is_consistent(var, value, assignment, constraints):
    # Sprawdzamy wszystkich sąsiadów wybranej zmiennej w grafie
    for neighbor in constraints[var]:
        # Jeśli sąsiad ma już przypisaną tę samą wartość, zwracamy fałsz (konflikt kolorów)
        if neighbor in assignment and assignment[neighbor] == value:
            return False
            
    # Jeśli nie ma konfliktów, wartość jest spójna
    return True

def backtrack(assignment, variables, domains, constraints):
    # Jeśli wszystkie zmienne mają przypisane wartości, zwracamy gotowy wynik
    if len(assignment) == len(variables):
        return assignment
    
    # 1.2 Założenie z zadania: przy przypisywaniu wartości jako pierwszy wybierany jest X2
    if not assignment:
        var = 'X2'
    else:
        # W kolejnych krokach używamy zasady minimalnych pozostałych wartości (MRV)
        var = mrv(variables, domains, assignment)

    # Próbujemy przypisać każdą dostępną wartość z domeny dla wybranej zmiennej
    for value in domains[var]:
        if is_consistent(var, value, assignment, constraints):
            # Jeśli wartość nie łamie ograniczeń, dodajemy ją do przypisania
            assignment[var] = value
            
            # Wywołujemy rekurencyjnie funkcję, aby kontynuować przeszukiwanie
            result = backtrack(assignment, variables, domains, constraints)
            if result:
                return result
            
            # Jeśli ścieżka nie prowadzi do rozwiązania, cofamy ten krok (backtracking)
            del assignment[var]
            
    # Zwracamy None, jeśli żadna ścieżka nie daje rozwiązania (wymusza powrót wyżej)
    return None

# 1.1 Definicja zbioru zmiennych
variables = ['X1', 'X2', 'X3']

# Definicja domen z obrazka
domains = {
    'X1': ['R', 'B', 'G'],
    'X2': ['R'],
    'X3': ['G']
}

# Wszystkie ograniczenia między zmiennymi (krawędzie grafu reprezentujące brak równości)
constraints = {
    'X1': ['X2', 'X3'],
    'X2': ['X1', 'X3'],
    'X3': ['X1', 'X2']
}

# 1.3 Uruchomienie programu, aby znaleźć rozwiązanie CSP
solution = backtrack({}, variables, domains, constraints)
# print("Rozwiązanie CSP:", solution)





## Zadanie 2
from itertools import combinations

# 2.1 Deklaracja systemu decyzyjnego z pierwszego zestawu (lub wykładu)
data = [
    ("o1", "wysoka", "bliski", "średni", "tak"),
    ("o2", "wysoka", "bliski", "średni", "tak"),
    ("o3", "wysoka", "bliski", "średni", "tak"),
    ("o4", "więcej niż średnia", "daleki", "silny", "nie pewne"),
    ("o5", "więcej niż średnia", "daleki", "silny", "nie"),
    ("o6", "więcej niż średnia", "daleki", "lekki", "nie"),
    ("o7", "wysoka", "bliski", "średni", "tak"),
    ("o8", "więcej niż średnia", "daleki", "lekki", "nie"),
    ("o9", "więcej niż średnia", "daleki", "lekki", "tak")
]

attributes = ["a1", "a2", "a3"]

def is_rule_consistent(target_obj, attrs_indices):
    # Decyzja (wynik) dla obiektu, dla którego budujemy regułę
    target_dec = target_obj[-1]
    
    # Przeszukujemy wszystkie obiekty w tabeli w poszukiwaniu sprzeczności
    for row in data:
        match = True
        # Sprawdzamy, czy wiersz ma takie same wartości dla deskryptorów w regule
        for i in attrs_indices:
            if row[i] != target_obj[i]:
                match = False
                break
        
        # Jeśli atrybuty są takie same, ale klasa decyzyjna jest inna -> reguła sprzeczna
        if match and row[-1] != target_dec:
            return False
            
    # Jeśli nie znaleźliśmy sprzecznych przypadków, reguła jest niesprzeczna
    return True

def sequential_covering():
    covered = set() # Zbiór ID obiektów, które zostały "wyrzucone z rozważań"
    rules = []
    
    # 2.2 Szukamy w obiektach systemu decyzyjnego reguł długości k (od 1 w górę)
    for k in range(1, len(attributes) + 1):
        # Generujemy wszystkie możliwe kombinacje atrybutów o danej długości k
        attr_combinations = list(combinations(range(1, 4), k))
        
        for obj in data:
            # Pamiętamy o tym, że wykluczony wcześniej obiekt nie tworzy już nowych reguł
            if obj[0] in covered:
                continue
                
            # Sprawdzamy kolejne kombinacje dla danego obiektu
            for comb in attr_combinations:
                if is_rule_consistent(obj, comb):
                    # Formatujemy regułę do czytelnego stringa
                    rule_cond = " AND ".join([f"{attributes[i-1]}={obj[i]}" for i in comb])
                    rules.append(f"IF {rule_cond} THEN dec={obj[-1]}")
                    
                    # Dany obiekt (i inne objęte tą samą regułą) wyrzucamy z rozważań
                    for row in data:
                        match = True
                        for i in comb:
                            if row[i] != obj[i]:
                                match = False
                                break
                        # Obiekty spełniające regułę lądują w zbiorze pokrytych (covered)
                        if match and row[-1] == obj[-1]:
                            covered.add(row[0])
                            
                    # Przerywamy pętlę atrybutów, by przejść do kolejnego niepokrytego obiektu
                    break 
    return rules

# Wypisanie znalezionych reguł
generated_rules = sequential_covering()
for rule in generated_rules:
    print(rule)