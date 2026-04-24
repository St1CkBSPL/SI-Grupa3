from itertools import combinations
import copy
import pygame

# ==================================================================================
# ZADANIE 1: CSP (Constraint Satisfaction Problem)
# ==================================================================================

import copy
import pygame


# --- LOGIKA ZADANIA 1 ---
def get_legal_values(var, assignment, domains, constraints):
    """Zwraca listę wartości z dziedziny, które nie kolidują z przypisanymi sąsiadami."""
    legal_values = []
    for value in domains[var]:
        conflict = False
        for neighbor in constraints[var]:
            if neighbor in assignment and assignment[neighbor] == value:
                conflict = True
                break
        if not conflict:
            legal_values.append(value)
    return legal_values


def solve_csp_logic():
    variables = ['X1', 'X2', 'X3']
    domains = {'X1': ['R', 'B', 'G'], 'X2': ['R'], 'X3': ['G']}
    constraints = {'X1': ['X2', 'X3'], 'X2': ['X1', 'X3'], 'X3': ['X1', 'X2']}
    steps = []

    def backtrack(assignment):
        # Zapisujemy kopię aktualnego stanu przypisań do historii kroków
        steps.append(copy.deepcopy(assignment))

        if len(assignment) == len(variables):
            return assignment

        # Wybór zmiennej: X2 wymuszone na początku, potem heurystyka MRV
        if not assignment:
            var = 'X2'
        else:
            unassigned = [v for v in variables if v not in assignment]
            # Wybieramy zmienną z najmniejszą liczbą dopuszczalnych wartości (MRV)
            var = min(unassigned, key=lambda v: len(get_legal_values(v, assignment, domains, constraints)))

        for value in domains[var]:
            # Sprawdzenie spójności (czy wartość nie koliduje z sąsiadami)
            if all(n not in assignment or assignment[n] != value for n in constraints[var]):
                assignment[var] = value
                if backtrack(assignment):
                    return assignment
                del assignment[var]
                steps.append(copy.deepcopy(assignment))
        return None

    backtrack({})
    # Zwracamy również domeny i więzy, by UI mogło je wykorzystać do analizy legalnych wartości
    return steps, domains, constraints


# --- WIZUALIZACJA ZADANIA 1 ---
def run_ui_zadanie_1(csp_data):
    csp_steps, full_domains, constraints = csp_data
    pygame.init()
    screen = pygame.display.set_mode((1100, 750))
    pygame.display.set_caption("ZADANIE 1 - Zaawansowana Wizualizacja CSP")

    # Paleta kolorów
    C = {
        'BG': (25, 25, 25),
        'TXT': (230, 230, 230),
        'BTN': (60, 100, 150),
        'R': (200, 50, 50),
        'G': (50, 200, 50),
        'B': (50, 50, 200),
        'GRAY': (60, 60, 60),
        'HL': (255, 255, 100)  # Highlight dla tekstu
    }

    f_xs = pygame.font.SysFont("Arial", 14)
    f_s = pygame.font.SysFont("Arial", 16)
    f_b = pygame.font.SysFont("Arial", 22, bold=True)

    step_idx = 0
    running = True

    # Pozycje węzłów na ekranie
    pos = {'X1': (550, 250), 'X2': (350, 500), 'X3': (750, 500)}

    while running:
        screen.fill(C['BG'])
        m_pos = pygame.mouse.get_pos()
        click = False

        for e in pygame.event.get():
            if e.type == pygame.QUIT: running = False
            if e.type == pygame.MOUSEBUTTONDOWN: click = True

        # Nagłówek i Instrukcja
        screen.blit(f_b.render("Zadanie 1: Analiza dopuszczalnych wartości (MRV)", True, C['TXT']), (50, 40))
        screen.blit(
            f_s.render("Poniżej widać dostępne kolory dla każdej zmiennej w danym stanie.", True, (160, 160, 160)),
            (50, 75))

        # Przyciski sterowania
        btn_next = pygame.Rect(450, 680, 200, 40)
        pygame.draw.rect(screen, C['BTN'], btn_next, border_radius=5)
        screen.blit(f_s.render(f"Krok: {step_idx} / {len(csp_steps) - 1}", True, C['TXT']),
                    (btn_next.x + 50, btn_next.y + 10))

        if click and btn_next.collidepoint(m_pos) and step_idx < len(csp_steps) - 1:
            step_idx += 1

        # Rysowanie krawędzi grafu
        for s, e in [('X1', 'X2'), ('X1', 'X3'), ('X2', 'X3')]:
            pygame.draw.line(screen, (100, 100, 100), pos[s], pos[e], 2)

        current_assignment = csp_steps[step_idx]

        # Rysowanie węzłów i informacji o kolorach
        for var_name, p in pos.items():
            assigned_val = current_assignment.get(var_name)

            # 1. Wyliczamy dopuszczalne wartości dla tego konkretnego stanu
            legal = get_legal_values(var_name, current_assignment, full_domains, constraints)

            # Rysowanie kółka węzła
            node_color = C.get(assigned_val, C['GRAY'])
            pygame.draw.circle(screen, node_color, p, 45)
            pygame.draw.circle(screen, (200, 200, 200), p, 45, 3)  # Obwódka

            # Nazwa zmiennej
            name_lbl = f_b.render(var_name, True, (255, 255, 255))
            screen.blit(name_lbl, (p[0] - 12, p[1] - 12))

            # 2. Wyświetlanie informacji o dziedzinie obok węzła
            info_x = p[0] + 55 if var_name != 'X3' else p[0] - 160
            info_y = p[1] - 30

            # Status przypisania
            status_txt = f"Wartość: {assigned_val if assigned_val else 'Brak'}"
            screen.blit(f_s.render(status_txt, True, C['HL'] if assigned_val else C['TXT']), (info_x, info_y))

            # Dostępne kolory (legalne)
            legal_txt = "Dostępne: " + (", ".join(legal) if legal else "KONFLIKT!")
            screen.blit(f_s.render(legal_txt, True, (100, 255, 100) if legal else (255, 100, 100)),
                        (info_x, info_y + 25))

            # Pełna dziedzina (dla porównania)
            domain_txt = f"Dziedzina: {full_domains[var_name]}"
            screen.blit(f_xs.render(domain_txt, True, (130, 130, 130)), (info_x, info_y + 45))
        pygame.display.flip()
    pygame.quit()


# ==================================================================================
# ZADANIE 2: ZBIORY PRZYBLIŻONE (Rough Sets)
# ==================================================================================

import pygame


# --- LOGIKA ZADANIA 2 ---
def calculate_rough_sets(data, attributes_indices, target_set_ids):
    """Oblicza klasy nierozróżnialności oraz przybliżenia dolne i górne."""
    classes = {}
    for row in data:
        obj_id = row[0]
        # Tworzymy krotkę cech, które decydują o podobieństwie
        attr_values = tuple(row[i] for i in attributes_indices)
        if attr_values not in classes: classes[attr_values] = []
        classes[attr_values].append(obj_id)

    target_set = set(target_set_ids)
    class_list = [sorted(objs) for objs in classes.values()]

    # Przybliżenie dolne: klasy, które w całości zawierają się w zbiorze docelowym
    lower = [c for c in class_list if set(c).issubset(target_set)]
    # Przybliżenie górne: klasy, które mają choć jeden element wspólny ze zbiorem docelowym
    upper = [c for c in class_list if not set(c).isdisjoint(target_set)]

    return {
        "classes": class_list,
        "lower": [obj for sub in lower for obj in sub],
        "upper": [obj for sub in upper for obj in sub],
        "target": target_set_ids
    }


def solve_rough_sets_logic():
    # Dane z tabeli Fig. 1 (o1 - o9)
    data = [
        ("o1", "wysoka", "bliski", "średni", "tak"), ("o2", "wysoka", "bliski", "średni", "tak"),
        ("o3", "wysoka", "bliski", "średni", "tak"), ("o4", "więcej niż średnia", "daleki", "silny", "nie pewne"),
        ("o5", "więcej niż średnia", "daleki", "silny", "nie"), ("o6", "więcej niż średnia", "daleki", "lekki", "nie"),
        ("o7", "wysoka", "bliski", "średni", "tak"), ("o8", "więcej niż średnia", "daleki", "lekki", "nie"),
        ("o9", "więcej niż średnia", "daleki", "lekki", "tak")
    ]
    # Definicje zbiorów z polecenia (5)
    X1 = ["o1", "o2", "o3", "o7", "o9"]
    X2 = ["o5", "o6", "o8"]

    return [
        {"title": "(i) Zbiór X2 dla A={a1,a2,a3}", "res": calculate_rough_sets(data, [1, 2, 3], X2)},
        {"title": "(ii) Zbiór X1 dla B={a1,a2}", "res": calculate_rough_sets(data, [1, 2], X1)},
        {"title": "(ii) Zbiór X2 dla B={a1,a2}", "res": calculate_rough_sets(data, [1, 2], X2)}
    ]


# --- WIZUALIZACJA ZADANIA 2 ---
def run_ui_zadanie_2(rs_results):
    pygame.init()
    screen = pygame.display.set_mode((1100, 750))
    pygame.display.set_caption("ZADANIE 2 - Wizualizacja Przybliżeń")

    C = {
        'BG': (25, 25, 25),
        'TXT': (230, 230, 230),
        'BTN': (60, 100, 150),
        'TARGET': (255, 215, 0),  # Złoty (obiekt docelowy)
        'LOWER': (40, 100, 40),  # Ciemnozielony (pewność)
        'UPPER_BRD': (100, 150, 255),  # Jasnoniebieski (możliwość)
        'OBJ_OUT': (100, 100, 100)  # Szary (poza zbiorem)
    }

    f_xs = pygame.font.SysFont("Arial", 14)
    f_s = pygame.font.SysFont("Arial", 16)
    f_b = pygame.font.SysFont("Arial", 22, bold=True)

    step_idx = 0
    running = True

    while running:
        screen.fill(C['BG'])
        m_pos = pygame.mouse.get_pos()
        click = False

        for e in pygame.event.get():
            if e.type == pygame.QUIT: running = False
            if e.type == pygame.MOUSEBUTTONDOWN: click = True

        # Sterowanie etapami (0-8, bo 3 podpunkty po 3 fazy)
        btn_next = pygame.Rect(450, 680, 200, 40)
        pygame.draw.rect(screen, C['BTN'], btn_next, border_radius=5)
        screen.blit(f_s.render(f"Następny Etap ({step_idx}/8)", True, C['TXT']), (btn_next.x + 40, btn_next.y + 10))

        if click and btn_next.collidepoint(m_pos) and step_idx < 8:
            step_idx += 1

        sub_problem = step_idx // 3  # który z 3 podpunktów
        phase = step_idx % 3  # 0: klasy, 1: dolne, 2: górne

        data_res = rs_results[sub_problem]
        screen.blit(f_b.render(data_res['title'], True, (255, 180, 50)), (50, 40))

        # Opis aktualnej fazy
        faza_txt = ["Faza: Podział na klasy nierozróżnialności",
                    "Faza: Wyznaczanie Przybliżenia Dolnego (Pewniaki)",
                    "Faza: Wyznaczanie Przybliżenia Górnego (Możliwości)"][phase]
        screen.blit(f_s.render(faza_txt, True, (180, 180, 180)), (50, 75))

        # Rysowanie kafelków (Klas)
        for idx, cl in enumerate(data_res['res']['classes']):
            # Rozmieszczenie siatki kafelków
            x_box = 70 + (idx % 3) * 330
            y_box = 120 + (idx // 3) * 180
            box_rect = pygame.Rect(x_box, y_box, 300, 150)

            # Logika kolorowania "pudełek"
            in_lower = set(cl).issubset(set(data_res['res']['target'])) and phase >= 1
            in_upper = not set(cl).isdisjoint(set(data_res['res']['target'])) and phase >= 2

            # Tło zielone dla dolnego przybliżenia
            if in_lower:
                pygame.draw.rect(screen, C['LOWER'], box_rect, border_radius=10)

            # Obramowanie niebieskie dla górnego przybliżenia
            border_col = C['UPPER_BRD'] if in_upper else (80, 80, 80)
            pygame.draw.rect(screen, border_col, box_rect, width=3, border_radius=10)

            screen.blit(f_xs.render(f"Klasa {idx + 1}", True, (150, 150, 150)), (x_box + 10, y_box + 10))

            # Rysowanie obiektów (kółek) wewnątrz klasy
            for o_idx, obj_name in enumerate(cl):
                o_x = x_box + 45 + (o_idx * 55)
                o_y = y_box + 75

                is_target = obj_name in data_res['res']['target']

                # Złoty kolor dla obiektów, które nas interesują
                obj_col = C['TARGET'] if is_target else C['OBJ_OUT']
                pygame.draw.circle(screen, obj_col, (o_x, o_y), 20)

                # Tekst z nazwą obiektu
                txt_col = (0, 0, 0) if is_target else (220, 220, 220)
                name_lbl = f_xs.render(obj_name, True, txt_col)
                screen.blit(name_lbl, (o_x - 8, o_y - 8))

        # Mała legenda na dole
        pygame.draw.circle(screen, C['TARGET'], (50, 650), 8)
        screen.blit(f_xs.render("= Element zbioru docelowego X", True, C['TXT']), (65, 642))
        pygame.draw.rect(screen, C['LOWER'], (50, 670, 15, 15))
        screen.blit(f_xs.render("= Przybliżenie Dolne", True, C['TXT']), (75, 670))
        pygame.draw.rect(screen, C['UPPER_BRD'], (50, 700, 15, 15), width=2)
        screen.blit(f_xs.render("= Przybliżenie Górne", True, C['TXT']), (75, 700))

        pygame.display.flip()
    pygame.quit()


# ==================================================================================
# ZADANIE 3: POKRYWANIE SEKWENCYJNE (Sequential Covering)
# ==================================================================================
def solve_sequential_covering_logic():
    """
    Znajduje reguły metodą pokrywania sekwencyjnego i zapisuje pełną historię
    kroków (co ułatwia wizualizację wykreślania wierszy z tabeli).
    """
    data = [
        ("o1", "wysoka", "bliski", "średni", "tak"),
        ("o2", "wysoka", "daleki", "średni", "tak"),
        ("o3", "więcej niż średnia", "daleki", "silny", "nie"),
        ("o4", "wysoka", "daleki", "silny", "nie"),
        ("o5", "więcej niż średnia", "bliski", "lekki", "tak"),
        ("o6", "więcej niż średnia", "daleki", "lekki", "tak"),
        ("o7", "więcej niż średnia", "bliski", "silny", "nie pewne"),
        ("o8", "wysoka", "bliski", "silny", "nie pewne"),
        ("o9", "wysoka", "bliski", "średni", "tak")
    ]
    attrs = ["a1", "a2", "a3"]
    covered = set()
    steps = []

    # 1. Szukamy reguł o długości k (od 1 do 3 atrybutów)
    for k in range(1, 4):
        for obj in data:
            if obj[0] in covered:
                continue

            # 2. Generujemy kombinacje atrybutów dla danego obiektu
            for comb in combinations(range(1, 4), k):
                # 3. Sprawdzamy niesprzeczność (czy wszystkie pasujące mają tę samą decyzję)
                is_consistent = True
                target_dec = obj[-1]
                for r in data:
                    match = all(r[i] == obj[i] for i in comb)
                    if match and r[-1] != target_dec:
                        is_consistent = False
                        break

                # 4. Jeśli reguła jest niesprzeczna, zapisujemy ją i pokryte obiekty
                if is_consistent:
                    rule_cond = " AND ".join([f"{attrs[i - 1]}='{obj[i]}'" for i in comb])
                    rule_text = f"IF {rule_cond} THEN {target_dec}"

                    newly_covered = []
                    for r in data:
                        if all(r[i] == obj[i] for i in comb) and r[-1] == target_dec and r[0] not in covered:
                            newly_covered.append(r[0])
                            covered.add(r[0])

                    steps.append({
                        'base_obj': obj[0],
                        'rule_text': rule_text,
                        'newly_covered': newly_covered,
                        'all_covered': list(covered),
                        'decision': target_dec
                    })
                    break  # Przechodzimy do następnego niepokrytego obiektu

        if len(covered) == len(data):
            break

    return data, steps


# --- WIZUALIZACJA ZADANIA 3 ---
def run_ui_zadanie_3(sc_data):
    raw_data, steps = sc_data

    pygame.init()
    screen = pygame.display.set_mode((1150, 750))
    pygame.display.set_caption("ZADANIE 3 - Odkrywanie Reguł (Wizualizacja Tabeli)")

    C = {
        'BG': (25, 25, 25),
        'TXT': (230, 230, 230),
        'BTN': (60, 100, 150),
        'DIM': (80, 80, 80),  # Wyszarzenie dla obiektów już pokrytych
        'HIGHLIGHT_TAK': (40, 120, 60),  # Zielony dla pozytywnych decyzji
        'HIGHLIGHT_NIE': (150, 50, 50),  # Czerwony dla negatywnych decyzji
        'TABLE_BG': (35, 35, 45)
    }

    f_s = pygame.font.SysFont("Arial", 14)
    f_m = pygame.font.SysFont("Arial", 16)
    f_b = pygame.font.SysFont("Arial", 22, bold=True)
    f_tbl = pygame.font.SysFont("Consolas", 15)  # Monospace dla czytelności tabeli

    step_idx = 0
    running = True

    # Kolumny tabeli (X pozycje)
    col_x = [40, 100, 300, 420, 540]
    headers = ["ID", "a1", "a2", "a3", "dec"]

    while running:
        screen.fill(C['BG'])
        m_pos = pygame.mouse.get_pos()
        click = False

        for e in pygame.event.get():
            if e.type == pygame.QUIT: running = False
            if e.type == pygame.MOUSEBUTTONDOWN: click = True

        screen.blit(f_b.render("Zadanie 3: Sekwencyjne Pokrywanie Obiektów", True, (255, 180, 50)), (40, 30))
        screen.blit(f_s.render("Tabela pokazuje, które obiekty są eliminowane przez nowo odkryte reguły.", True,
                               (170, 170, 170)), (40, 60))

        # --- Przycisk "Następny krok" ---
        btn_next = pygame.Rect(450, 680, 250, 40)
        pygame.draw.rect(screen, C['BTN'], btn_next, border_radius=5)

        if step_idx < len(steps):
            btn_txt = f"Odkryj regułę {step_idx + 1}/{len(steps)}"
        else:
            btn_txt = "Wszystkie obiekty pokryte!"

        screen.blit(f_m.render(btn_txt, True, C['TXT']), (btn_next.x + 30, btn_next.y + 10))

        if click and btn_next.collidepoint(m_pos) and step_idx < len(steps):
            step_idx += 1

        # Pobieranie stanu na dany krok
        current_step = steps[step_idx - 1] if step_idx > 0 else None
        previously_covered = steps[step_idx - 2]['all_covered'] if step_idx > 1 else []
        newly_covered = current_step['newly_covered'] if current_step else []

        # --- Rysowanie Tabeli Danych (Lewa strona) ---
        tbl_y_start = 120
        # Nagłówki
        pygame.draw.rect(screen, (50, 50, 70), (30, tbl_y_start, 580, 30), border_radius=4)
        for i, h in enumerate(headers):
            screen.blit(f_b.render(h, True, (255, 255, 255)), (col_x[i], tbl_y_start + 3))

        # Wiersze
        for i, row in enumerate(raw_data):
            obj_id = row[0]
            y = tbl_y_start + 40 + (i * 35)

            # Logika kolorowania wiersza
            row_bg = C['TABLE_BG']
            txt_col = C['TXT']

            if obj_id in previously_covered:
                row_bg = C['BG']
                txt_col = C['DIM']  # Wyszarzamy, bo już załatwione w poprzednich krokach
            elif obj_id in newly_covered:
                # Wyróżniamy obiekty pokryte w TYM konkretnym kroku
                row_bg = C['HIGHLIGHT_TAK'] if current_step['decision'] == 'tak' else C['HIGHLIGHT_NIE']
                txt_col = (255, 255, 255)

            pygame.draw.rect(screen, row_bg, (30, y, 580, 30), border_radius=4)
            if obj_id in newly_covered:
                pygame.draw.rect(screen, (255, 255, 255), (30, y, 580, 30), width=1, border_radius=4)

            # Rysowanie komórek
            for j, val in enumerate(row):
                screen.blit(f_tbl.render(str(val), True, txt_col), (col_x[j], y + 6))

        # --- Rysowanie Wygenerowanych Reguł (Prawa strona) ---
        rule_start_x = 650
        screen.blit(f_b.render("Wygenerowane Reguły:", True, C['TXT']), (rule_start_x, 120))

        for i in range(step_idx):
            step = steps[i]
            ry = 160 + (i * 60)

            # Pudełko dla reguły
            is_active = (i == step_idx - 1)  # Podświetl najnowszą
            bg_col = (60, 65, 80) if is_active else (40, 45, 60)
            pygame.draw.rect(screen, bg_col, (rule_start_x, ry, 460, 50), border_radius=5)
            if is_active:
                pygame.draw.rect(screen, (200, 200, 200), (rule_start_x, ry, 460, 50), width=2, border_radius=5)

            # Tekst reguły
            dec_color = (150, 255, 150) if step['decision'] == 'tak' else (255, 150, 150)
            screen.blit(f_m.render(f"Baza {step['base_obj']}: {step['rule_text']}", True, dec_color),
                        (rule_start_x + 10, ry + 8))

            # Informacja o pokryciu
            cov_txt = f"Pokrywa obiekty: {', '.join(step['newly_covered'])}"
            screen.blit(f_s.render(cov_txt, True, (180, 180, 180)), (rule_start_x + 10, ry + 28))

        pygame.display.flip()
    pygame.quit()
# ==================================================================================
# PANEL GŁÓWNY (WYBÓR MODUŁU DO URUCHOMIENIA)
# ==================================================================================
if __name__ == "__main__":
    print("\n--- SYSTEMY DECYZYJNE - MENU ---")
    print("Obliczanie logiki w tle...")

    # Wywołanie funkcji logicznych niezależnie od renderowania
    dane_zad_1 = solve_csp_logic()
    dane_zad_2 = solve_rough_sets_logic()
    dane_zad_3 = solve_sequential_covering_logic()

    while True:
        print("\nKtóre zadanie chcesz zwizualizować?")
        print("1. Zadanie 1: CSP")
        print("2. Zadanie 2: Zbiory Przybliżone")
        print("3. Zadanie 3: Reguły Sekwencyjne")
        print("0. Wyjście")

        wybor = input("Twój wybór: ")

        if wybor == '1':
            run_ui_zadanie_1(dane_zad_1)
        elif wybor == '2':
            run_ui_zadanie_2(dane_zad_2)
        elif wybor == '3':
            run_ui_zadanie_3(dane_zad_3)
        elif wybor == '0':
            print("Koniec programu.")
            break
        else:
            print("Nieprawidłowy wybór, spróbuj ponownie.")
