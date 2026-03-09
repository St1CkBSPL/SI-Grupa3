import statistics
import random
import copy
import math
import csv
from collections import Counter

data = []
classes = []

with open("diabetes.txt", "r") as file:
    for line in file:
        line = line.strip()
        if not line:
            continue
        row = line.split()
        attributes = [float(x) for x in row[:-1]]
        decision_class = row[-1]

        data.append(attributes)
        classes.append(decision_class)

if not data:
    print("Plik jest pusty lub niepoprawnie wczytany.")
    exit()

num_attributes = len(data[0])


# Funkcja pomocnicza wykorzystywana w Zadaniu 3
def get_col(attr_idx, filter_cls=None, dataset=data):
    if filter_cls is None:
        return [row[attr_idx] for row in dataset]
    return [dataset[i][attr_idx] for i in range(len(dataset)) if classes[i] == filter_cls]


print("--- Wyniki ---")

# ZADANIE 3a) Wypisujemy istniejące w systemie symbole klas decyzyjnych
unique_classes = set(classes)
print(f"\n3a) Symbole klas decyzyjnych: {unique_classes}")
print("     Wyjaśnienie: Użyto rzutowania na strukturę 'set' (zbiór), która z definicji przechowuje tylko unikalne wartości, automatycznie odrzucając duplikaty z listy klas.")

# ZADANIE 3b) Wielkości klas decyzyjnych (liczby obiektów w klasach)
class_sizes = Counter(classes)
print("\n3b) Wielkości klas decyzyjnych:")
for cls, size in class_sizes.items():
    print(f"   - Klasa '{cls}': {size} obiektów")
print("     Wyjaśnienie: Zastosowano narzędzie 'Counter' z biblioteki 'collections', które przechodzi przez listę klas i automatycznie zlicza liczbę wystąpień każdego symbolu.")

# ZADANIE 3c) Minimalne i maksymalne wartości poszczególnych atrybutów numerycznych
print("\n3c) Minimalne i maksymalne wartości atrybutów:")
for i in range(num_attributes):
    col = get_col(i)
    print(f"   Atrybut {i + 1}: min = {min(col)}, max = {max(col)}")
print("     Wyjaśnienie: Dla każdej kolumny wyciągnięto jej dane do osobnej listy, a następnie użyto wbudowanych funkcji Pythona 'min()' oraz 'max()', by znaleźć skrajne wartości.")

# ZADANIE 3d) Dla każdego atrybutu wypisujemy liczbę różnych dostępnych wartości
print("\n3d) Liczba różnych dostępnych wartości dla każdego atrybutu:")
for i in range(num_attributes):
    print(f"   Atrybut {i + 1}: {len(set(get_col(i)))} unikalnych wartości")
print("     Wyjaśnienie: Podobnie jak w 3a, zamieniono listę wartości z kolumny na 'set', co usunęło powtórzenia, a funkcja 'len()' sprawdziła, ile unikalnych elementów zostało.")

# ZADANIE 3e) Dla każdego atrybutu wypisujemy listę wszystkich różnych dostępnych wartości
print("\n3e) Lista wszystkich różnych dostępnych wartości (skrócona do 10 dla czytelności):")
for i in range(num_attributes):
    uniq = sorted(list(set(get_col(i))))
    print(f"   Atrybut {i + 1}: {uniq[:10]} ... (łącznie {len(uniq)})")
print("     Wyjaśnienie: Wyciągnięto unikalne wartości poprzez 'set()', przekonwertowano z powrotem na listę i ułożono rosnąco funkcją 'sorted()'. Wydrukowano fragment poprzez tzw. slicing (cięcie list).")

# ZADANIE 3f) Odchylenie standardowe dla atrybutów w całym systemie i w klasach
print("\n3f) Odchylenie standardowe w całym systemie i klasach decyzyjnych:")
for i in range(num_attributes):
    col_all = get_col(i)
    std_all = statistics.stdev(col_all) if len(col_all) > 1 else 0.0
    print(f"   Atrybut {i + 1}:")
    print(f"      - Cały system: {std_all:.4f}")

    for cls in unique_classes:
        col_class = get_col(i, filter_cls=cls)
        std_class = statistics.stdev(col_class) if len(col_class) > 1 else 0.0
        print(f"      - Klasa '{cls}': {std_class:.4f}")
print("     Wyjaśnienie: Wykorzystano funkcję 'stdev' z wbudowanego modułu 'statistics'. Wykonano to w podwójnej pętli: raz dla całej kolumny, a potem dla wartości przefiltrowanych po konkretnej klasie.")

# ZADANIE 4

# ZADANIE 4a) Wygeneruj 10% braków i napraw metodą wartości średniej
print("\n4a) Generowanie i naprawa brakujących wartości (10%):")
data_4a = copy.deepcopy(data)
total_cells = len(data_4a) * num_attributes
missing_count = int(0.1 * total_cells)

all_coords = [(r, c) for r in range(len(data_4a)) for c in range(num_attributes)]
random.seed(42)
missing_coords = random.sample(all_coords, missing_count)

for r, c in missing_coords:
    data_4a[r][c] = '?'
print(f"   Wygenerowano {missing_count} znaków zapytania ('?').")

for c in range(num_attributes):
    known_values = [data_4a[r][c] for r in range(len(data_4a)) if data_4a[r][c] != '?']
    col_mean = sum(known_values) / len(known_values) if known_values else 0.0
    for r in range(len(data_4a)):
        if data_4a[r][c] == '?':
            data_4a[r][c] = col_mean
print("   Zastąpiono braki danych średnią wartością dla atrybutów numerycznych.")
print("     Wyjaśnienie: Obliczono liczbę równą 10% wszystkich komórek, wylosowano ich współrzędne i wpisano tam '?'. Następnie obliczono średnią dla każdej kolumny (omijając '?') i wstawiono ją w puste miejsca.")
print("     podgląd danych (pierwsze 3 wiersze po naprawie braków):")
for row in data_4a[:3]:
    print(f"      {[round(x, 4) if isinstance(x, float) else x for x in row]}")

# ZADANIE 4b) Znormalizuj atrybuty numeryczne na przedziały: <-1, 1>, <0, 1>, <-10, 10>
print("\n4b) Normalizacja na zadane przedziały:")


def normalize_data(input_data, a, b):
    norm_data = copy.deepcopy(input_data)
    for c in range(num_attributes):
        col_values = [norm_data[r][c] for r in range(len(norm_data))]
        min_a = min(col_values)
        max_a = max(col_values)

        for r in range(len(norm_data)):
            if max_a - min_a == 0:
                norm_data[r][c] = a
            else:
                norm_data[r][c] = ((norm_data[r][c] - min_a) * (b - a) / (max_a - min_a)) + a
    return norm_data


data_norm_1 = normalize_data(data, -1, 1)
data_norm_2 = normalize_data(data, 0, 1)
data_norm_3 = normalize_data(data, -10, 10)
print("   Zakończono normalizację. Zbiory wynikowe: data_norm_1, data_norm_2, data_norm_3.")
print("     Wyjaśnienie: Zdefiniowano uniwersalną funkcję, która znajduje minimum i maksimum dla danej kolumny, a potem przelicza każdą wartość według podanego w zadaniu matematycznego wzoru na normalizację min-max.")
print("     podgląd danych (pierwszy wiersz dla każdej normalizacji):")
print(f"      Przedział <-1, 1>:   {[round(x, 4) for x in data_norm_1[0]]}")
print(f"      Przedział <0, 1>:    {[round(x, 4) for x in data_norm_2[0]]}")
print(f"      Przedział <-10, 10>: {[round(x, 4) for x in data_norm_3[0]]}")

# ZADANIE 4c) Dokonaj standaryzacji wartości numerycznych (średnia = 0, wariancja = 1)
print("\n4c) Standaryzacja wartości numerycznych:")
data_std = copy.deepcopy(data)

for c in range(num_attributes):
    col_values = [data_std[r][c] for r in range(len(data_std))]
    mean_a = sum(col_values) / len(col_values)
    std_dev = math.sqrt(sum((x - mean_a) ** 2 for x in col_values) / len(col_values))

    for r in range(len(data_std)):
        if std_dev != 0:
            data_std[r][c] = (data_std[r][c] - mean_a) / std_dev
        else:
            data_std[r][c] = 0.0
print("   Standaryzacja zakończona (nowa średnia atrybutów wynosi 0, a wariancja 1).")
print("     Wyjaśnienie: Dla każdej kolumny wyliczono wartość średnią oraz odchylenie standardowe ze wzoru na populację. Następnie od każdej komórki odjęto średnią i podzielono przez to odchylenie, tworząc tzw. Z-score.")
print("     podgląd danych (pierwsze 3 wiersze po standaryzacji):")
for row in data_std[:3]:
    print(f"      {[round(x, 4) for x in row]}")

# ZADANIE 4d) Przeformatuj dane z pliku Churn_Modelling.csv, zamień atrybut Geography na Dummy Variables

print("\n4d) Dummy Variables - plik Churn_Modelling.csv")

churn_data = []
headers = []

try:
    with open("Churn_Modelling.csv", "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        for row in reader:
            churn_data.append(row)

    if "Geography" in headers:
        geo_idx = headers.index("Geography")

        unique_geographies = sorted(list(set(row[geo_idx] for row in churn_data)))

        # Skasuj jeden z nowych atrybutów aby uniknąć pułapki Dummy Variables (wchłanianie)
        dropped_geo = unique_geographies[0]
        dummy_geographies = unique_geographies[1:]

        print(f"   Znalezione unikalne wartości: {unique_geographies}")
        print(f"   Skasowany atrybut (uniknięcie wchłaniania): '{dropped_geo}'")
        print(f"   Nowe atrybuty Dummy Variables: {[f'Geography_{geo}' for geo in dummy_geographies]}")

        new_headers = headers[:geo_idx] + [f"Geography_{geo}" for geo in dummy_geographies] + headers[geo_idx + 1:]

        new_churn_data = []
        for row in churn_data:
            geo_val = row[geo_idx]
            dummy_vals = [1 if geo_val == geo else 0 for geo in dummy_geographies]
            new_row = row[:geo_idx] + dummy_vals + row[geo_idx + 1:]
            new_churn_data.append(new_row)

        print("   Sukces: Zakończono transformację atrybutu 'Geography'.")
        print("     Wyjaśnienie: Odczytano plik CSV, zlokalizowano kolumnę 'Geography' i wydobyto jej unikalne nazwy. Skasowano pierwszą wartość (referencyjną, by uniknąć współliniowości), a dla reszty stworzono nowe kolumny wstawiając '1', jeśli wartość się zgadzała, lub '0', jeśli nie (One-Hot Encoding).")

        print("\n   podgląd danych (transformacja nagłówków i pierwszego wiersza):")
        print(f"      Stare nagłówki (fragment wokół indeksu {geo_idx}): {headers[max(0, geo_idx - 1):geo_idx + 2]}")
        print(
            f"      Nowe nagłówki (fragment po wklejeniu): {new_headers[max(0, geo_idx - 1):geo_idx + len(dummy_geographies) + 1]}")
        print(f"      Stary wiersz 1 (fragment): {churn_data[0][max(0, geo_idx - 1):geo_idx + 2]}")
        print(
            f"      Nowy wiersz 1 (fragment):  {new_churn_data[0][max(0, geo_idx - 1):geo_idx + len(dummy_geographies) + 1]}")

    else:
        print("   Błąd: Nie znaleziono kolumny 'Geography' w pliku.")

except FileNotFoundError:
    print(
        "   Błąd: Brak pliku 'Churn_Modelling.csv'. Upewnij się, że plik znajduje się w tym samym katalogu co skrypt.")