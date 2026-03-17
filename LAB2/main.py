import heapq
from collections import deque


# ==========================================
# ZADANIE 1: Świat odkurzacza (BFS)
# ==========================================
def task1_vacuum_bfs():
    print("--- ZADANIE 1: Świat odkurzacza (BFS) ---")

    # Stan: (lokalizacja_agenta, czy_A_brudne, czy_B_brudne)
    initial_state = ('A', True, True)

    print(f"   [PRZED] Stan początkowy:")
    print(f"      Lokalizacja robota: {initial_state[0]}")
    print(f"      Kwadrat A brudny: {initial_state[1]}")
    print(f"      Kwadrat B brudny: {initial_state[2]}\n")

    # Kolejka przechowuje krotki: (aktualny_stan, sciezka_akcji)
    queue = deque([(initial_state, [])])
    visited = {initial_state}
    step = 0

    while queue:
        current_state, path = queue.popleft()
        loc, a_dirty, b_dirty = current_state
        step += 1

        # Wyświetlanie pierwszych 3 kroków przeszukiwania
        if step <= 3:
            print(f"   [KROK {step}] Analizuję stan z kolejki:")
            print(f"      Pozycja: {loc}, Brud w A: {a_dirty}, Brud w B: {b_dirty}")
            print(f"      Ścieżka prowadząca do tego stanu: {path if path else 'Brak (start)'}\n")

        # Test celu: oba pola czyste
        if not a_dirty and not b_dirty:
            print(f"   [PO] Stan docelowy osiągnięty po sprawdzeniu {step} stanów:")
            print(f"      Lokalizacja robota: {loc} (nie ma znaczenia dla celu)")
            print(f"      Kwadrat A brudny: {a_dirty}")
            print(f"      Kwadrat B brudny: {b_dirty}")
            print(f"      -> Znaleziona sekwencja akcji: {path}")

            print(
                "\n   -> Wyjaśnienie: Algorytm BFS na każdym kroku wyciąga z kolejki stan i generuje wszystkie możliwe w nim akcje. Dzięki wydrukom kroków widać, jak algorytm sprawdza najpierw stany oddalone o 0 akcji, potem o 1 akcję itd.\n")
            return path

        # Generowanie akcji
        actions = [
            ('W lewo', ('A', a_dirty, b_dirty)),
            ('W prawo', ('B', a_dirty, b_dirty))
        ]

        if loc == 'A' and a_dirty:
            actions.append(('Ssać', ('A', False, b_dirty)))
        elif loc == 'B' and b_dirty:
            actions.append(('Ssać', ('B', a_dirty, False)))

        for action_name, next_state in actions:
            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, path + [action_name]))


# ==========================================
# ZADANIE 2: 8-Puzzle (A* z heurystyką Manhattan)
# ==========================================
class PuzzleState:
    def __init__(self, board, g_cost, path):
        self.board = board
        self.g_cost = g_cost
        self.path = path
        self.h_cost = self.calculate_manhattan()
        self.f_cost = self.g_cost + self.h_cost

    def calculate_manhattan(self):
        goal_positions = {
            1: (0, 0), 2: (0, 1), 3: (0, 2),
            4: (1, 0), 5: (1, 1), 6: (1, 2),
            7: (2, 0), 8: (2, 1)
        }
        distance = 0
        for i in range(3):
            for j in range(3):
                val = self.board[i][j]
                if val != 0:
                    goal_r, goal_c = goal_positions[val]
                    distance += abs(i - goal_r) + abs(j - goal_c)
        return distance

    def __lt__(self, other):
        return self.f_cost < other.f_cost

    def get_empty_pos(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return i, j


def get_neighbors(state):
    neighbors = []
    r, c = state.get_empty_pos()
    directions = {'Góra': (-1, 0), 'Dół': (1, 0), 'Lewo': (0, -1), 'Prawo': (0, 1)}

    for action, (dr, dc) in directions.items():
        new_r, new_c = r + dr, c + dc
        if 0 <= new_r < 3 and 0 <= new_c < 3:
            new_board = [row[:] for row in state.board]
            new_board[r][c], new_board[new_r][new_c] = new_board[new_r][new_c], new_board[r][c]
            neighbors.append((action, new_board))

    return neighbors


def print_board(board, prefix=""):
    for row in board:
        formatted_row = ['[]' if x == 0 else f"[{x}]" for x in row]
        print(f"{prefix}{''.join(formatted_row)}")


def task2_a_star_search():
    print("--- ZADANIE 2: Gra 8-puzzle (A*) ---")

    initial_board = [
        [0, 1, 3],
        [4, 2, 5],
        [7, 8, 6]
    ]

    goal_board = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]

    print("   [PRZED] Stan początkowy (zero to '[]'):")
    print_board(initial_board, "      ")
    print()

    start_state = PuzzleState(initial_board, 0, [])
    open_set = []
    heapq.heappush(open_set, start_state)
    visited = set()
    step = 0

    while open_set:
        current_state = heapq.heappop(open_set)
        board_tuple = tuple(tuple(row) for row in current_state.board)
        step += 1

        # Wyświetlanie pierwszych 5 kroków algorytmu A*
        if step <= 5:
            print(
                f"   [KROK {step}] Wybrano z kolejki stan z oceną f={current_state.f_cost} (Kroki g={current_state.g_cost}, Heurystyka h={current_state.h_cost}):")
            print_board(current_state.board, "      ")
            print(f"      Wykonane ruchy: {current_state.path if current_state.path else 'Brak'}\n")

        if current_state.board == goal_board:
            print("   [PO] Stan docelowy osiągnięty!")
            print_board(current_state.board, "      ")
            print(f"      -> Całkowity koszt (liczba kroków): {current_state.g_cost}")
            print(f"      -> Sekwencja akcji pustego pola: {current_state.path}")

            print(
                "\n   -> Wyjaśnienie: Z logów krokowych widać, że w każdym kroku algorytm wyciągał z kolejki planszę z najmniejszym szacowanym kosztem 'f'. Ponieważ nasza heurystyka (odległość Manhattan) jest bardzo dobra, algorytm szedł prosto do celu, bez gubienia się w ślepych zaułkach.\n")
            return current_state.path

        if board_tuple in visited:
            continue

        visited.add(board_tuple)

        for action, new_board in get_neighbors(current_state):
            new_state = PuzzleState(new_board, current_state.g_cost + 1, current_state.path + [action])
            heapq.heappush(open_set, new_state)


# ==========================================
# ZADANIE 3: Trywialna gra (Minimax z Alpha-Beta)
# ==========================================
game_tree = {
    'A': ['B', 'C', 'D'],
    'B': [3, 12, 8],
    'C': [2, 4, 6],
    'D': [14, 5, 2]
}


def alpha_beta_pruning(node, alpha, beta, is_maximizing, depth=0):
    indent = "      " + ("   " * depth)

    if isinstance(node, int):
        print(f"{indent}[Liść] Analizowana wypłata: {node}")
        return node, []

    print(f"{indent}[Węzeł {node}] Gracz {'MAX' if is_maximizing else 'MIN'} ocenia możliwości...")

    if is_maximizing:
        max_eval = -float('inf')
        best_path = []

        for child in game_tree[node]:
            eval_val, path = alpha_beta_pruning(child, alpha, beta, False, depth + 1)
            if eval_val > max_eval:
                max_eval = eval_val
                best_path = [child] + path

            alpha = max(alpha, eval_val)
            if beta <= alpha:
                print(
                    f"{indent}--> [ODCIĘCIE ALFA-BETA] Odcięto pozostałe gałęzie po sprawdzeniu {child}! (Beta: {beta} <= Alfa: {alpha})")
                break

        print(f"{indent}Węzeł {node} otrzymuje wartość: {max_eval}")
        return max_eval, best_path

    else:
        min_eval = float('inf')
        best_path = []

        for child in game_tree[node]:
            eval_val, path = alpha_beta_pruning(child, alpha, beta, True, depth + 1)
            if eval_val < min_eval:
                min_eval = eval_val
                best_path = [child] + path

            beta = min(beta, eval_val)
            if beta <= alpha:
                print(
                    f"{indent}--> [ODCIĘCIE ALFA-BETA] Odcięto pozostałe gałęzie po sprawdzeniu {child}! (Beta: {beta} <= Alfa: {alpha})")
                break

        print(f"{indent}Węzeł {node} otrzymuje wartość: {min_eval}")
        return min_eval, best_path


def task3_minimax():
    print("--- ZADANIE 3: Trywialna gra (Minimax + Alpha-Beta Pruning) ---")

    print("   [PRZED] Struktura drzewa:")
    print(f"      Węzeł startowy A -> Gałęzie: {game_tree['A']}")
    print(f"      Gałąź B prowadzi do liści: {game_tree['B']}")
    print(f"      Gałąź C prowadzi do liści: {game_tree['C']}")
    print(f"      Gałąź D prowadzi do liści: {game_tree['D']}\n")

    print("   [ANALIZA DRZEWA - KROKI]:")
    optimal_value, optimal_path = alpha_beta_pruning('A', -float('inf'), float('inf'), True)

    print(f"\n   [PO] Zakończenie analizy:")
    print(f"      -> Wynik optymalny dla gracza MAX: {optimal_value}")
    print(f"      -> Optymalna strategia (wybór ścieżki): A -> {optimal_path[0]}")

    print(
        "\n   -> Wyjaśnienie: Z logów analizy drzewa widać, w jakiej kolejności algorytm odwiedza węzły. Kiedy gracz MIN (węzły B, C, D) wybiera minimalną wartość, zapisuje tę informację jako parametr Beta. Gracz MAX przekazuje te obostrzenia w dół, a kiedy okazuje się, że jakaś nowa ścieżka już teraz jest gorsza od tego co zagwarantował sobie wcześniej MAX (Alfa), algorytm natychmiast ją odcina (Pruning), co wyraźnie widać w wypisanych krokach.")


# ==========================================
# Uruchomienie wszystkich zadań
# ==========================================
if __name__ == "__main__":
    task1_vacuum_bfs()
    task2_a_star_search()
    task3_minimax()