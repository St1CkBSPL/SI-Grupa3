## Zadanie 1

def count_legal_values(var, assignment, domains, constraints):
    # Inicjujemy licznik dopuszczalnych wartości dla sprawdzanej zmiennej
    legal_count = 0
    for value in domains[var]:
        conflict = False
        # Weryfikujemy każdego sąsiada w grafie ograniczeń
        for neighbor in constraints[var]:
            # Jeśli sąsiad ma już tę samą przypisaną wartość, zgłaszamy konflikt
            if neighbor in assignment and assignment[neighbor] == value:
                conflict = True
                break
        # Jeśli dana wartość nie łamie więzów (brak konfliktu), zwiększamy pulę legalnych opcji
        if not conflict:
            legal_count += 1
    return legal_count


def mrv(variables, domains, assignment, constraints):
    # Wyodrębniamy zmienne, które wciąż czekają na przypisanie
    unassigned = [v for v in variables if v not in assignment]

    # Wybieramy tę zmienną, która ma najmniej legalnych opcji (Minimum Remaining Values).
    # Funkcja count_legal_values działa tu jako dynamiczne sprawdzanie w przód (Forward Checking).
    chosen_var = min(unassigned, key=lambda v: count_legal_values(v, assignment, domains, constraints))
    print(
        f"  [MRV] Algorytm wybrał zmienną {chosen_var}, ponieważ została jej najmniejsza liczba dopuszczalnych wartości.")
    return chosen_var


def is_consistent(var, value, assignment, constraints):
    # Sprawdzamy, czy przypisywana wartość nie została już zajęta przez połączonego sąsiada
    for neighbor in constraints[var]:
        if neighbor in assignment and assignment[neighbor] == value:
            print(f"  [BŁĄD] Konflikt! Sąsiad {neighbor} ma już przypisaną wartość '{value}'.")
            return False
    return True


def backtrack(assignment, variables, domains, constraints, step=None):
    # Inicjalizacja licznika kroków dla czytelności logów
    if step is None:
        step = [1]

    print(f"\n--- KROK {step[0]} ---")
    print(f"Aktualny stan przypisań: {assignment}")
    step[0] += 1

    # Warunek stopu: wszystkie zmienne otrzymały poprawne wartości
    if len(assignment) == len(variables):
        print("  -> SUKCES! Znaleziono pełne i spójne rozwiązanie.")
        return assignment

    # Krok 1.2 z zadania: wymuszamy wybór X2 na samym początku przeszukiwania
    if not assignment:
        var = 'X2'
        print(f"  [START] Zgodnie z wytycznymi z zadania, zaczynamy od zmiennej {var}.")
    else:
        # Dla kolejnych kroków uruchamiamy heurystykę MRV
        var = mrv(variables, domains, assignment, constraints)

    # Iterujemy po dostępnej domenie wybranej zmiennej
    for value in domains[var]:
        print(f"  -> Próba przypisania: {var} = '{value}'")

        # Jeśli wartość jest lokalnie spójna z resztą grafu
        if is_consistent(var, value, assignment, constraints):
            print(f"  [OK] Wartość '{value}' dla {var} jest dopuszczalna.")
            assignment[var] = value

            # Rekurencyjnie zagłębiamy się w drzewo przeszukiwania
            result = backtrack(assignment, variables, domains, constraints, step)

            # Jeśli wywołanie rekurencyjne zwróciło wynik, propagujemy go w górę
            if result:
                return result

            # Ślepy zaułek – cofamy przypisanie (mechanizm backtracking) i próbujemy innej wartości
            print(f"  [COFANIE] Droga z {var}='{value}' okazała się ślepym zaułkiem. Następuje wycofanie.")
            del assignment[var]

    # Brak rozwiązania w tej konkretnej gałęzi poszukiwań
    print(f"  [PORAŻKA] Wyczerpano wszystkie bezpieczne opcje dla zmiennej {var}.")
    return None


# Definicja problemu: zmienne, dziedziny oraz ograniczenia (krawędzie grafu z zadania 1.1)
variables = ['X1', 'X2', 'X3']
domains = {
    'X1': ['R', 'B', 'G'],
    'X2': ['R'],
    'X3': ['G']
}
constraints = {
    'X1': ['X2', 'X3'],
    'X2': ['X1', 'X3'],
    'X3': ['X1', 'X2']
}

print("=== START ALGORYTMU CSP ===")
solution = backtrack({}, variables, domains, constraints)
print("\nOSTATECZNY WYNIK:", solution)

## Zadanie 2
from itertools import combinations

# Baza wiedzy - system decyzyjny (tabela z przykładami o1-o9)
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

# Nazwy naszych atrybutów warunkowych
attributes = ["a1", "a2", "a3"]


def is_rule_consistent(target_obj, attrs_indices):
    # Pobieramy docelową klasę decyzyjną sprawdzanego obiektu (ostatni element w krotce)
    target_dec = target_obj[-1]

    # Przeszukujemy całą tabelę w poszukiwaniu ewentualnych sprzeczności
    for row in data:
        match = True
        # Sprawdzamy, czy badany wiersz ma takie same wartości dla wytypowanych atrybutów
        for i in attrs_indices:
            if row[i] != target_obj[i]:
                match = False
                break

        # Jeśli znaleźliśmy wiersz o takich samych cechach, ale INNEJ decyzji końcowej - reguła upada
        if match and row[-1] != target_dec:
            return False

    # Jeśli pętla przeszła bez przeszkód, reguła jest niesprzeczna
    return True


def sequential_covering():
    covered = set()  # Zbiór przechowujący identyfikatory obiektów już "wyjaśnionych" regułami
    rules = []  # Lista na gotowe, niesprzeczne reguły

    # 2.2 Zgodnie z teorią, szukamy reguł zaczynając od rzędu 1 aż do wyczerpania liczby atrybutów
    for k in range(1, len(attributes) + 1):
        print(f"\n======================================")
        print(f"--- ETAP: Szukanie reguł rzędu {k} ---")
        print(f"======================================")

        # Generujemy wszystkie możliwe kombinacje atrybutów o długości k
        attr_combinations = list(combinations(range(1, 4), k))

        for obj in data:
            # Obiekt, który został już opisany wcześniejszą regułą, nie może stanowić bazy dla nowej
            if obj[0] in covered:
                continue

            rule_found = False
            for comb in attr_combinations:
                print(f"  Analiza {obj[0]} z cechami na indeksach {comb}...")

                # Jeśli kombinacja atrybutów pozwala wyodrębnić jednoznaczną decyzję:
                if is_rule_consistent(obj, comb):
                    # Budujemy czytelny ciąg znaków opisujący warunek IF...
                    rule_cond = " AND ".join([f"{attributes[i - 1]}='{obj[i]}'" for i in comb])
                    formatted_rule = f"IF {rule_cond} THEN dec='{obj[-1]}'"

                    covered_by_this = []

                    # Szukamy, ile jeszcze innych obiektów "łapie się" na tę nową regułę
                    for row in data:
                        match = True
                        for i in comb:
                            if row[i] != obj[i]:
                                match = False
                                break
                        # Dodajemy je do puli wyeliminowanych obiektów
                        if match and row[-1] == obj[-1]:
                            covered.add(row[0])
                            covered_by_this.append(row[0])

                    rules.append(f"{obj[0]}: {formatted_rule}")
                    print(f"  [ZNALEZIONO!] -> {formatted_rule}")
                    print(f"  [AKCJA] Wyrzucamy z dalszych rozważań obiekty: {', '.join(covered_by_this)}\n")

                    rule_found = True
                    # Skoro znaleźliśmy dobrą regułę dla tego obiektu, przerywamy sprawdzanie innych kombinacji
                    break

                    # Jeśli dla danej długości k nie udało się znaleźć reguły
            if not rule_found:
                print(f"  [BRAK] Obiekt {obj[0]} - nie znaleziono reguły niesprzecznej rzędu {k}.\n")

        # Warunek wcześniejszego zatrzymania - jeśli wyeliminowaliśmy już całą tabelę, kończymy
        if len(covered) == len(data):
            print("\n*** SUKCES: Wszystkie obiekty w tabeli zostały z powodzeniem pokryte. ***")
            break

    return rules


print("=== START ALGORYTMU POKRYWANIA SEKWENCYJNEGO ===")
generated_rules = sequential_covering()

print("\n=== PODSUMOWANIE WYGENEROWANYCH REGUŁ ===")
for r in generated_rules:
    print(r)

# ==================================================================================
# SEKCJA WIZUALIZACJI INTERAKTYWNEJ (PYGAME)
# ==================================================================================
import pygame
import time


def start_animated_visualization(csp_final, rules_final):
    pygame.init()
    screen = pygame.display.set_mode((1100, 650))
    pygame.display.set_caption("Animowana Wizualizacja Algorytmów SI")

    # Kolory i Fonty
    COLORS = {'R': (255, 60, 60), 'G': (60, 255, 60), 'B': (60, 100, 255), 'BG': (30, 30, 30), 'TXT': (240, 240, 240)}
    BTN_COLOR = (70, 130, 180)
    BTN_HOVER = (100, 150, 200)
    f_small = pygame.font.SysFont("Segoe UI", 18)
    f_bold = pygame.font.SysFont("Segoe UI", 24, bold=True)

    # Współrzędne grafu CSP
    nodes = {'X1': (250, 180), 'X2': (100, 450), 'X3': (400, 450)}

    # Definicja przycisku "Następny krok"
    btn_rect = pygame.Rect(180, 550, 160, 45)

    # Sekwencja animacji CSP (odtwarzamy kroki na podstawie logiki)
    csp_steps = [
        {},
        {'X2': 'R'},
        {'X2': 'R', 'X3': 'G'},
        {'X2': 'R', 'X3': 'G', 'X1': 'B'}
    ]

    # Przygotowanie danych do animacji reguł
    parsed_rules = []
    for r in rules_final:
        parts = r.split(": ")
        obj_id = parts[0]
        rule_content = parts[1]
        parsed_rules.append({'id': obj_id, 'text': rule_content})

    clock = pygame.time.Clock()
    step_csp = 0
    step_rules = 0
    last_update = time.time()
    mode = "CSP"

    running = True
    while running:
        screen.fill(COLORS['BG'])
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Obsługa kliknięcia myszką
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if mode == "CSP" and btn_rect.collidepoint(mouse_pos):
                    if step_csp < len(csp_steps) - 1:
                        step_csp += 1
                    else:
                        # Jeśli wyczerpaliśmy kroki CSP, płynnie przechodzimy do ZAD 2
                        mode = "RULES"
                        last_update = time.time()

        # --- LOGIKA TIMERA ANIMACJI (TYLKO DLA REGUŁ) ---
        now = time.time()
        if mode == "RULES":
            if now - last_update > 2.0:
                if step_rules < len(parsed_rules):
                    step_rules += 1
                last_update = now

        # --- RYSOWANIE GRAFU CSP ---
        pygame.draw.line(screen, (100, 100, 100), (550, 50), (550, 600), 1)
        title_csp = f_bold.render("1. Wizualizacja CSP", True, COLORS['TXT'])
        screen.blit(title_csp, (50, 30))

        # Krawędzie
        for start, end in [('X1', 'X2'), ('X1', 'X3'), ('X2', 'X3')]:
            pygame.draw.line(screen, (150, 150, 150), nodes[start], nodes[end], 3)

        # Węzły
        current_csp = csp_steps[min(step_csp, len(csp_steps) - 1)]
        for name, pos in nodes.items():
            val = current_csp.get(name)
            col = COLORS.get(val, (80, 80, 80))
            pygame.draw.circle(screen, col, pos, 45)
            pygame.draw.circle(screen, (200, 200, 200), pos, 45, 3)

            label = f_bold.render(name, True, (255, 255, 255))
            screen.blit(label, (pos[0] - 15, pos[1] - 15))
            if val:
                val_txt = f_small.render(f"Value: {val}", True, (255, 255, 255))
                screen.blit(val_txt, (pos[0] - 30, pos[1] + 50))

        # --- RYSOWANIE PRZYCISKU (TYLKO DLA CSP) ---
        if mode == "CSP":
            # Zmiana koloru po najechaniu myszką
            current_btn_color = BTN_HOVER if btn_rect.collidepoint(mouse_pos) else BTN_COLOR
            pygame.draw.rect(screen, current_btn_color, btn_rect, border_radius=8)
            pygame.draw.rect(screen, (200, 200, 200), btn_rect, width=2, border_radius=8)

            btn_txt = "Następny krok" if step_csp < len(csp_steps) - 1 else "Zakończ CSP"
            btn_label = f_small.render(btn_txt, True, (255, 255, 255))
            screen.blit(btn_label, (btn_rect.x + 25, btn_rect.y + 10))

            info_txt = f_small.render(f"Krok: {step_csp}/{len(csp_steps) - 1}", True, (150, 150, 150))
            screen.blit(info_txt, (btn_rect.x + 40, btn_rect.y + 55))

        # --- RYSOWANIE REGUŁ ---
        title_rules = f_bold.render("2. Pokrywanie Sekwencyjne", True, COLORS['TXT'])
        screen.blit(title_rules, (600, 30))

        for i in range(step_rules):
            r = parsed_rules[i]
            y_pos = 100 + (i * 60)

            pygame.draw.rect(screen, (50, 50, 70), (580, y_pos, 480, 50), border_radius=5)
            r_label = f_small.render(f"Base {r['id']}: {r['text']}", True,
                                     (100, 255, 100) if "tak" in r['text'] else (255, 100, 100))
            screen.blit(r_label, (595, y_pos + 12))

        status_txt = "Oczekuję na kliknięcie..." if mode == "CSP" else (
            "Animacja reguł..." if step_rules < len(parsed_rules) else "Zakończono wizualizację.")
        status_render = f_small.render(status_txt, True, (180, 180, 180))
        screen.blit(status_render, (450, 610))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    print("\n[INFO] Zamykanie konsoli... Uruchamiam interaktywne okno Pygame.")
    start_animated_visualization(solution, generated_rules)