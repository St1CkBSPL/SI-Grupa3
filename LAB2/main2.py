import heapq
from collections import deque

# ==========================================
# ZADANIE 1: BFS (świat odkurzacza)
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

        # kroki (ograniczone)
        if step <= 6:
            print(f"Krok {step}:")
            print(f"  Robot jest w: {loc}")
            print(f"  Stan: A={'brudne' if a_dirty else 'czyste'}, B={'brudne' if b_dirty else 'czyste'}")
            print(f"  Ścieżka: {path if path else 'start'}\n")

        # cel
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


# ==========================================
# ZADANIE 2: A* (8-puzzle)
# ==========================================
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


# ==========================================
# ZADANIE 3: Minimax + Alpha-Beta
# ==========================================
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
        return node

    print(f"{indent}Węzeł {node} ({'MAX' if maximizing else 'MIN'})")

    if maximizing:
        value = float('-inf')
        for child in game_tree[node]:
            print(f"{indent}→ Sprawdzam {child}")
            value = max(value, alpha_beta(child, alpha, beta, False, depth + 1))
            alpha = max(alpha, value)
            print(f"{indent}  MAX = {value}")

            if beta <= alpha:
                print(f"{indent}  Przycięcie")
                break
        return value
    else:
        value = float('inf')
        for child in game_tree[node]:
            print(f"{indent}→ Sprawdzam {child}")
            value = min(value, alpha_beta(child, alpha, beta, True, depth + 1))
            beta = min(beta, value)
            print(f"{indent}  MIN = {value}")

            if beta <= alpha:
                print(f"{indent}  Przycięcie")
                break
        return value


def task3_minimax():
    print("\n--- ZADANIE 3: Minimax ---")

    result = alpha_beta('A', float('-inf'), float('inf'), True)

    print("\nWynik:", result)
    print("Opis:")
    print("- MAX maksymalizuje wynik, MIN minimalizuje")
    print("- algorytm zakłada optymalną grę obu stron")
    print("- alpha-beta przycina zbędne gałęzie\n")


# ==========================================
# MAIN
# ==========================================
if __name__ == "__main__":
    task1_vacuum_bfs()
    task2_a_star()
    task3_minimax()