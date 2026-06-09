import numpy as np


# zadanie 2 podpunkt 3
print(" \nzadanie 2 podpunkt 3 ")

# Macierz przechowująca dane. Pierwsza kolumna to "bias" (zawsze 1), kolejne to nasze wejścia x1 i x2 tzn tabela prawdy
macierz_wejsc = np.array([
    [1, 0, 0],
    [1, 0, 1],
    [1, 1, 0],
    [1, 1, 1]
])

# Oczekiwany wynik sieci dla wejść
oczekiwane_wyniki = np.array([0, 0, 1, 0])

# parametry startowe
wagi_perceptronu = np.array([0.5, 0.5, 0.5])
wspolczynnik_uczenia = 0.5
liczba_epok = 10 # liczba epok ustawiona arbitralnie by zabezpieczyć się przed zapętleniem


# idziemy po każdej epoce
for epoka in range(liczba_epok):
    liczba_bledow = 0 # resetujemy licznik błędów
    print(f"\nEpoka {epoka + 1}:")

    for i in range(len(macierz_wejsc)):
        aktywne_wejscie = macierz_wejsc[i] # wyciagamy z macierzy po jednym wierszu

        # Obliczanie sumy ważonej
        suma_wazona = np.dot(wagi_perceptronu, aktywne_wejscie) #przykładowo 0,5 * 1 + 0,5 * 0 + 0,5 * 0 = 0,5 dla wiersza 1 w 1 epoce

        # jeżeli suma jest dodatnia to wyjście = 1 w innym przypadku 0
        wyjscie_perceptronu = 1 if suma_wazona > 0 else 0

        # obliczanie błeu
        blad = oczekiwane_wyniki[i] - wyjscie_perceptronu

        # Jeśli sieć popełniła błąd, trzeba poprawić wagi
        if blad != 0:
            # Wzór: stara_waga + (współczynnik * błąd * sygnał_wejściowy)
            wagi_perceptronu = wagi_perceptronu + wspolczynnik_uczenia * blad * aktywne_wejscie
            liczba_bledow += 1

        print(
            f" Wejście (x1,x2): {aktywne_wejscie[1:]}, Oczekiwane: {oczekiwane_wyniki[i]}, Wynik programu: {wyjscie_perceptronu}, Zaktualizowane wagi: {wagi_perceptronu}, liczba błędów: {liczba_bledow}")

    if liczba_bledow == 0:
        print(f"Sieć nauczyła się bezbłędnie w epoce {epoka + 1}. Wagi perceptronu to: {wagi_perceptronu}")
        break


# Zadanie 2 podpunkt 4

print("\n=== ZADANIE 2 (iv): Sieć wielowarstwowa (Backpropagation) ===")


# funkcja normalizująca wyniki między 0 a 1
def funkcja_aktywacji_sigmoid(x):
    return 1 / (1 + np.exp(-x))


# Pochodna potrzebna przy liczeniu propagacji wstecznej
def pochodna_funkcji_sigmoid(wyjscie_z_neuronu):
    return wyjscie_z_neuronu * (1 - wyjscie_z_neuronu)


# dane wejściowe
sygnaly_wejsciowe = np.array([0.6, 0.1]) # pierwszy przykład
oczekiwany_wynik_sieci = np.array([1.0, 0.0])  # Wymagany format na dwa neurony na wyjściu
szybkosc_uczenia = 0.1

# Macierz wag pomiędzy początkiem sieci (wejściem) a środkiem (warstwą ukrytą)
wagi_wejscie_ukryta = np.array([
    [0.1, 0.0, 0.3],  # wagi sygnału x1 idące do trzech neuronów w środku
    [-0.2, 0.2, -0.4]  # wagi sygnału x2 idące do trzech neuronów w środku
])
bias_warstwy_ukrytej = np.array([0.1, 0.2, 0.5])  # strzałki niebieskie na rysunku wskazujące bias każdego z środkowych neuronów

# Macierz wag pomiędzy środkiem (warstwą ukrytą) a końcem sieci (wyjściem)
wagi_ukryta_wyjscie = np.array([
    [-0.4, 0.2],  # wagi idące od pierwszego środkowego neurona do wyjść
    [0.1, -0.1],  # wagi idące od drugiego środkowego neurona do wyjść
    [0.6, -0.2]  # wagi idące od trzeciego środkowego neurona do wyjść
])
bias_warstwy_wyjsciowej = np.array([-0.1, 0.6]) # strzałki niebieskie na rysunku wskazujące bias każdego z końcowych neuronów


# Propagacja w przód
# ====================================
# Obliczanie sumy ważonej
suma_wazona_ukryta = np.dot(sygnaly_wejsciowe, wagi_wejscie_ukryta) + bias_warstwy_ukrytej # suma ważona środkowych neurownów + ich bias
sygnal_z_warstwy_ukrytej = funkcja_aktywacji_sigmoid(suma_wazona_ukryta) # normalizacja wyniku do między 0 a 1

suma_wazona_wyjsciowa = np.dot(sygnal_z_warstwy_ukrytej, wagi_ukryta_wyjscie) + bias_warstwy_wyjsciowej # suma ważona końcowych neurownów + ich bias
ostateczny_wynik_sieci = funkcja_aktywacji_sigmoid(suma_wazona_wyjsciowa) # normalizacja wyniku do między 0 a 1

print("\nPropagacja w przód")
print(f"Wyjścia policzone przez środkową warstwę: {np.round(sygnal_z_warstwy_ukrytej, 4)}")
print(f"Ostateczny wynik sieci: {np.round(ostateczny_wynik_sieci, 4)}")
# ====================================

# Propagacja wsteczna (analiza błędu)
# ====================================
blad_na_samym_wyjsciu = ostateczny_wynik_sieci - oczekiwany_wynik_sieci # obliczenie błędu na wyjściu
delta_wyjsciowa = blad_na_samym_wyjsciu * pochodna_funkcji_sigmoid(ostateczny_wynik_sieci) # obliczenie delty błędu wyjścia

blad_w_srodku_sieci = np.dot(delta_wyjsciowa, wagi_ukryta_wyjscie.T) # obliczenie błędu w wyjściu środkowych neuronów
delta_ukryta = blad_w_srodku_sieci * pochodna_funkcji_sigmoid(sygnal_z_warstwy_ukrytej) # obliczenie delty błędu wyjścia środkowych neuronów


# Korekta wszystkich wag

nowe_wagi_ukryta_wyjscie = wagi_ukryta_wyjscie - szybkosc_uczenia * np.outer(sygnal_z_warstwy_ukrytej, delta_wyjsciowa) # obliczenie nowych wag  neuronów końcowych uwzględniając błąd oraz szybkośc uczenia
nowy_bias_warstwy_wyjsciowej = bias_warstwy_wyjsciowej - szybkosc_uczenia * delta_wyjsciowa # korekcja biasu neuronów wyjściowych

nowe_wagi_wejscie_ukryta = wagi_wejscie_ukryta - szybkosc_uczenia * np.outer(sygnaly_wejsciowe, delta_ukryta) # obliczenie nowych wag neuronów środkowych uwzględniając błąd oraz szybkośc uczenia
nowy_bias_warstwy_ukrytej = bias_warstwy_ukrytej - szybkosc_uczenia * delta_ukryta # korekcja biasu neuronów środkowych

print("\n--- Zmiany wag")
print("Nowe wartości biasów neuronów końcowych")
print(np.round(nowy_bias_warstwy_wyjsciowej, 4))
print("Nowe wagi na trasie: środek -> wyjście:")
print(np.round(nowe_wagi_ukryta_wyjscie, 4))

print("\nNowe wartości biasów neuronów środkowych:")
print(np.round(nowy_bias_warstwy_ukrytej, 4))
print("Nowe wagi na trasie: wejście -> środek:")
print(np.round(nowe_wagi_wejscie_ukryta, 4))