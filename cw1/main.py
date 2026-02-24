import statistics
from collections import Counter

# Inicjalizacja list na dane
data = []
classes = []

# Odczyt pliku
with open("diabetes.txt", "r") as file:
    for line in file:
        line = line.strip()
        if not line:
            continue

        # Dzielenie linii na elementy po białych znakach (spacje/tabulatory)
        row = line.split()

        # Zakładamy, że wszystkie kolumny oprócz ostatniej to atrybuty numeryczne
        attributes = [float(x) for x in row[:-1]]
        decision_class = row[-1]  # Ostatnia kolumna to klasa decyzyjna (zostawiamy jako tekst/znak)

        data.append(attributes)
        classes.append(decision_class)

if not data:
    print("Plik jest pusty lub niepoprawnie wczytany.")
    exit()

num_attributes = len(data[0])

# --- a) Symbole klas decyzyjnych ---
unique_classes = set(classes)
print(f"a) Symbole klas decyzyjnych: {unique_classes}\n")

# --- b) Wielkości klas decyzyjnych ---
class_sizes = Counter(classes)
print("b) Wielkości klas decyzyjnych:")
for cls, size in class_sizes.items():
    print(f"   Klasa '{cls}': {size} obiektów")
print()


# Funkcja pomocnicza do pobierania całej kolumny danego atrybutu (z opcjonalnym filtrem klasy)
def get_attribute_column(attr_index, filter_class=None):
    if filter_class is None:
        return [row[attr_index] for row in data]
    else:
        return [data[i][attr_index] for i in range(len(data)) if classes[i] == filter_class]


# --- c) Minimalne i maksymalne wartości poszczególnych atrybutów ---
print("c) Minimalne i maksymalne wartości atrybutów:")
for i in range(num_attributes):
    col = get_attribute_column(i)
    print(f"   Atrybut {i + 1}: min = {min(col)}, max = {max(col)}")
print()

# --- d) Liczba różnych dostępnych wartości dla każdego atrybutu ---
print("d) Liczba różnych dostępnych wartości:")
for i in range(num_attributes):
    col = get_attribute_column(i)
    unique_vals = set(col)
    print(f"   Atrybut {i + 1}: {len(unique_vals)} unikalnych wartości")
print()

# --- e) Lista wszystkich różnych dostępnych wartości dla każdego atrybutu ---
print("e) Lista różnych dostępnych wartości:")
for i in range(num_attributes):
    col = get_attribute_column(i)
    unique_vals = sorted(list(set(col)))
    # Wyświetlamy tylko początek listy, by nie zaśmiecać konsoli przy dużej ilości danych
    print(f"   Atrybut {i + 1}: {unique_vals[:10]} ... (łącznie {len(unique_vals)})")
print()

# --- f) Odchylenie standardowe w całym systemie i w klasach ---
print("f) Odchylenie standardowe (próby):")
for i in range(num_attributes):
    col_all = get_attribute_column(i)

    # Obliczenie dla całego systemu
    std_all = statistics.stdev(col_all) if len(col_all) > 1 else 0.0
    print(f"   Atrybut {i + 1}:")
    print(f"      - Cały system: {std_all:.4f}")

    # Obliczenie dla poszczególnych klas
    for cls in unique_classes:
        col_class = get_attribute_column(i, filter_class=cls)
        std_class = statistics.stdev(col_class) if len(col_class) > 1 else 0.0
        print(f"      - Klasa '{cls}': {std_class:.4f}")