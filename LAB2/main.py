import heapq
from collections import deque
import pygame
import sys
import time


# ==========================================
# WARSTWA LOGIKI (Twoje algorytmy)
# ==========================================

def task1_vacuum_bfs():
    print("\n--- ZADANIE 1: BFS ---")
    initial_state = ('A', True, True)
    queue = deque([(initial_state, [])])
    visited = {initial_state}
    step = 0

    while queue:
        (loc, a_dirty, b_dirty), path = queue.popleft()
        step += 1

        if step <= 6:
            print(f"Krok {step}:")
            print(f"  Robot jest w: {loc}")
            print(f"  Stan: A={'brudne' if a_dirty else 'czyste'}, B={'brudne' if b_dirty else 'czyste'}")
            print(f"  Ścieżka: {path if path else 'start'}\n")

        if not a_dirty and not b_dirty:
            print("Wynik:", path)
            print("Opis:")
            print("- BFS przegląda stany poziomami")
            print("- znajduje najkrótszą sekwencję ruchów\n")
            return path

        actions = [
            ('W lewo', ('A', a_dirty, b_dirty)),
            ('W prawo', ('B', a_dirty, b_dirty))
        ]

        if loc == 'A' and a_dirty:
            actions.append(('Ssać', ('A', False, b_dirty)))
        elif loc == 'B' and b_dirty:
            actions.append(('Ssać', ('B', a_dirty, False)))

        for action, state in actions:
            if state not in visited:
                visited.add(state)
                queue.append((state, path + [action]))


class PuzzleState:
    def __init__(self, board, g, path):
        self.board = board
        self.g = g
        self.path = path
        self.h = self.manhattan()
        self.f = self.g + self.h

    def manhattan(self):
        goal = {
            1: (0, 0), 2: (0, 1), 3: (0, 2),
            4: (1, 0), 5: (1, 1), 6: (1, 2),
            7: (2, 0), 8: (2, 1)
        }
        return sum(
            abs(i - goal[val][0]) + abs(j - goal[val][1])
            for i in range(3)
            for j in range(3)
            if (val := self.board[i][j]) != 0
        )

    def __lt__(self, other):
        return self.f < other.f

    def empty(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return i, j


def get_neighbors(state):
    moves = {'Góra': (-1, 0), 'Dół': (1, 0), 'Lewo': (0, -1), 'Prawo': (0, 1)}
    r, c = state.empty()
    result = []

    for move, (dr, dc) in moves.items():
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            new = [row[:] for row in state.board]
            new[r][c], new[nr][nc] = new[nr][nc], new[r][c]
            result.append((move, new))
    return result


def task2_a_star():
    print("\n--- ZADANIE 2: A* ---")
    start = [[0, 1, 3], [4, 2, 5], [7, 8, 6]]
    goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    open_set = []
    heapq.heappush(open_set, PuzzleState(start, 0, []))
    visited = set()
    step = 0

    while open_set:
        state = heapq.heappop(open_set)
        step += 1

        if step <= 6:
            print(f"Krok {step}:")
            print(f"  Koszt (g): {state.g}")
            print(f"  Heurystyka (h): {state.h}")
            print(f"  f = g + h: {state.f}")
            print(f"  Ruchy: {state.path if state.path else 'start'}\n")

        if state.board == goal:
            print("Ruchy:", state.path)
            print("Koszt:", state.g)
            print("Opis:")
            print("- A* wybiera najmniejsze f = g + h")
            print("- g = wykonane ruchy, h = odległość do celu")
            print("- znajduje optymalne rozwiązanie\n")
            return state.path

        board_tuple = tuple(tuple(r) for r in state.board)
        if board_tuple in visited:
            continue

        visited.add(board_tuple)

        for move, board in get_neighbors(state):
            heapq.heappush(open_set, PuzzleState(board, state.g + 1, state.path + [move]))


game_tree = {
    'A': ['B', 'C', 'D'],
    'B': [3, 12, 8],
    'C': [2, 4, 6],
    'D': [14, 5, 2]
}


def alpha_beta(node, alpha, beta, maximizing, depth=0):
    indent = "  " * depth
    if isinstance(node, int):
        print(f"{indent}Liść: wartość = {node}")
        return node, []

    print(f"{indent}Węzeł {node} ({'MAX' if maximizing else 'MIN'})")

    if maximizing:
        value = float('-inf')
        best_path = []
        for child in game_tree[node]:
            print(f"{indent}→ Sprawdzam {child}")
            child_val, path = alpha_beta(child, alpha, beta, False, depth + 1)
            if child_val > value:
                value = child_val
                best_path = [child] + path
            alpha = max(alpha, value)
            print(f"{indent}  MAX = {value}")

            if beta <= alpha:
                print(f"{indent}  Przycięcie")
                break
        return value, best_path
    else:
        value = float('inf')
        best_path = []
        for child in game_tree[node]:
            print(f"{indent}→ Sprawdzam {child}")
            child_val, path = alpha_beta(child, alpha, beta, True, depth + 1)
            if child_val < value:
                value = child_val
                best_path = [child] + path
            beta = min(beta, value)
            print(f"{indent}  MIN = {value}")

            if beta <= alpha:
                print(f"{indent}  Przycięcie")
                break
        return value, best_path


def task3_minimax():
    print("\n--- ZADANIE 3: Minimax ---")
    val, path = alpha_beta('A', float('-inf'), float('inf'), True)
    print("\nWynik:", val)
    print("Opcja:", path)
    return val, path


# ==========================================
# WARSTWA INTERFEJSU (Wizualizacje Pygame)
# ==========================================

# Wspólne kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (50, 150, 255)
RED = (255, 50, 50)
GREEN = (50, 200, 50)
BROWN = (139, 69, 19)


def init_pygame():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Wizualizacja Algorytmów AI")
    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 32)
    return screen, font, small_font


def wait_for_close():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return


def visualize_vacuum(path):
    screen, font, small_font = init_pygame()
    loc, a_dirty, b_dirty = 'A', True, True

    # Tworzymy klatki animacji na podstawie ścieżki
    frames = [(loc, a_dirty, b_dirty, "START")]
    for action in path:
        if action == 'W lewo':
            loc = 'A'
        elif action == 'W prawo':
            loc = 'B'
        elif action == 'Ssać':
            if loc == 'A': a_dirty = False
            if loc == 'B': b_dirty = False
        frames.append((loc, a_dirty, b_dirty, action))

    for frame in frames:
        current_loc, cur_a_dirty, cur_b_dirty, action_name = frame
        screen.fill(WHITE)

        # Tytuł
        title = font.render(f"Zadanie 1: Świat odkurzacza - Akcja: {action_name}", True, BLACK)
        screen.blit(title, (50, 50))

        # Pokoje
        pygame.draw.rect(screen, GRAY, (150, 200, 200, 200), 2)
        pygame.draw.rect(screen, GRAY, (450, 200, 200, 200), 2)
        screen.blit(font.render("A", True, BLACK), (240, 150))
        screen.blit(font.render("B", True, BLACK), (540, 150))

        # Brud
        if cur_a_dirty:
            pygame.draw.circle(screen, BROWN, (250, 300), 30)
        if cur_b_dirty:
            pygame.draw.circle(screen, BROWN, (550, 300), 30)

        # Odkurzacz
        v_x = 200 if current_loc == 'A' else 500
        pygame.draw.rect(screen, BLUE, (v_x, 250, 100, 100))
        screen.blit(small_font.render("ROBOT", True, WHITE), (v_x + 10, 290))

        pygame.display.flip()
        time.sleep(1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

    screen.blit(small_font.render("Zakończono. Naciśnij ESC lub zamknij okno.", True, RED), (50, 500))
    pygame.display.flip()
    wait_for_close()


def visualize_puzzle(path):
    screen, font, small_font = init_pygame()
    board = [[0, 1, 3], [4, 2, 5], [7, 8, 6]]

    def draw_board(brd, step_name):
        screen.fill(WHITE)
        title = font.render(f"Zadanie 2: 8-Puzzle - Akcja: {step_name}", True, BLACK)
        screen.blit(title, (50, 50))

        start_x, start_y = 250, 150
        size = 100
        for i in range(3):
            for j in range(3):
                val = brd[i][j]
                rect = (start_x + j * size, start_y + i * size, size, size)
                if val != 0:
                    pygame.draw.rect(screen, BLUE, rect)
                    pygame.draw.rect(screen, BLACK, rect, 3)
                    text = font.render(str(val), True, WHITE)
                    screen.blit(text, (start_x + j * size + 35, start_y + i * size + 35))
                else:
                    pygame.draw.rect(screen, GRAY, rect)
                    pygame.draw.rect(screen, BLACK, rect, 3)

        pygame.display.flip()

    draw_board(board, "START")
    time.sleep(1)

    moves = {'Góra': (-1, 0), 'Dół': (1, 0), 'Lewo': (0, -1), 'Prawo': (0, 1)}
    for action in path:
        # Znajdź 0
        r, c = -1, -1
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    r, c = i, j
                    break

        dr, dc = moves[action]
        nr, nc = r + dr, c + dc
        board[r][c], board[nr][nc] = board[nr][nc], board[r][c]

        draw_board(board, action)
        time.sleep(0.8)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

    screen.blit(small_font.render("Rozwiązane! Naciśnij ESC lub zamknij okno.", True, RED), (50, 500))
    pygame.display.flip()
    wait_for_close()


def visualize_tree(path):
    screen, font, small_font = init_pygame()
    screen.fill(WHITE)

    title = font.render("Zadanie 3: Minimax z odcięciami", True, BLACK)
    screen.blit(title, (50, 30))

    # Ręczne koordynaty dla trywialnego drzewa z zadania
    nodes = {
        'A': (400, 100),
        'B': (200, 250), 'C': (400, 250), 'D': (600, 250),
        'B1': (100, 450), 'B2': (200, 450), 'B3': (300, 450),
        'C1': (350, 450), 'C2': (400, 450), 'C3': (450, 450),
        'D1': (550, 450), 'D2': (600, 450), 'D3': (650, 450),
    }

    edges = [
        ('A', 'B'), ('A', 'C'), ('A', 'D'),
        ('B', 'B1'), ('B', 'B2'), ('B', 'B3'),
        ('C', 'C1'), ('C', 'C2'), ('C', 'C3'),
        ('D', 'D1'), ('D', 'D2'), ('D', 'D3')
    ]

    labels = {
        'B1': '3', 'B2': '12', 'B3': '8',
        'C1': '2', 'C2': '4', 'C3': '6',
        'D1': '14', 'D2': '5', 'D3': '2'
    }

    # Określenie wybranej ścieżki by podświetlić
    # path wygląda zazwyczaj: ['B', 3] - modyfikujemy by znaleźć liść graficznie
    highlight = ['A']
    if 'B' in path: highlight.extend(['B', 'B1'])  # B1 to liść z 3

    # Rysowanie krawędzi
    for start, end in edges:
        color = GREEN if (start in highlight and end in highlight) else BLACK
        width = 5 if color == GREEN else 2
        pygame.draw.line(screen, color, nodes[start], nodes[end], width)

    # Rysowanie węzłów
    for name, pos in nodes.items():
        color = BLUE if len(name) == 1 else GRAY
        pygame.draw.circle(screen, color, pos, 30)
        pygame.draw.circle(screen, BLACK, pos, 30, 2)

        lbl = labels.get(name, name)
        txt = small_font.render(lbl, True, WHITE if color == BLUE else BLACK)
        txt_rect = txt.get_rect(center=pos)
        screen.blit(txt, txt_rect)

    # Oznaczenie odcięć na twardo dla edukacji wizualnej z zadania
    screen.blit(small_font.render("X Odcięcie Alpha-Beta", True, RED), (380, 350))
    pygame.draw.line(screen, RED, (380, 270), (450, 400), 4)

    screen.blit(small_font.render("Najlepsza decyzja: A -> B", True, GREEN), (50, 520))
    screen.blit(small_font.render("Naciśnij ESC lub zamknij okno.", True, RED), (50, 560))

    pygame.display.flip()
    wait_for_close()


# ==========================================
# MAIN
# ==========================================
if __name__ == "__main__":
    # Zadanie 1
    path1 = task1_vacuum_bfs()
    visualize_vacuum(path1)

    # Zadanie 2
    path2 = task2_a_star()
    visualize_puzzle(path2)

    # Zadanie 3
    val3, path3 = task3_minimax()
    visualize_tree(path3)

    pygame.quit()
    sys.exit()