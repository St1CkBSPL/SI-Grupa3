from itertools import combinations
import copy
import pygame


#  zadanie 1 logika
def pobierz_dozwolone_wartosci(zmienna, przypisanie, dziedziny, ograniczenia):

    # Tworzymy pustą listę, do której będziemy wrzucać kolory, które są dozwolone
    dozwolone_wartosci = []

    # Bierzemy każdy możliwy kolor z dziedziny naszej zmiennej (np. 'R', 'B', 'G')
    for wartosc in dziedziny[zmienna]:
        # Zakładamy optymistycznie, że nie ma z nim żadnego konfliktu
        konflikt = False

        # Sprawdzamy sąsiadów węzła
        for sasiad in ograniczenia[zmienna]:
            # Jeśli sąsiad jest pokolorowany ORAZ ma taki sam kolor jak testowany
            if sasiad in przypisanie and przypisanie[sasiad] == wartosc:
                # to znaczy, że mamy konflikt. Przerywamy sprawdzanie.
                konflikt = True
                break
        # Jeśli po sprawdzeniu sąsiadów nie było konfliktu, dodajemy kolor do puli legalnych
        if not konflikt:
            dozwolone_wartosci.append(wartosc)

    return dozwolone_wartosci


def logika_csp():

    # dane z polecenia (zmienne, dostępne kolory i graf połączeń)
    zmienne = ['X1', 'X2', 'X3']
    dziedziny = {'X1': ['R', 'B', 'G'], 'X2': ['R'], 'X3': ['G']}
    ograniczenia = {'X1': ['X2', 'X3'], 'X2': ['X1', 'X3'], 'X3': ['X1', 'X2']}

    # zapisujemy kroki algorytmu
    kroki = []

    def szukaj_rekurencyjnie(przypisanie):
        # Na starcie robimy głęboką kopię obecnego stanu i wrzucamy do historii kroków
        kroki.append(copy.deepcopy(przypisanie))

        # Warunek stopu: jeśli pokolorowaliśmy wszystkie węzły, to algorytm się kończy
        if len(przypisanie) == len(zmienne):
            return przypisanie

        # wymuszamy start od zmiennej X2.
        if not przypisanie:
            obecna_zmienna = 'X2'
        else:
            # mrv
            # Tworzymy listę jeszcze niepokolorowanych węzłów i wybieramy ten węzeł, który ma najmniej "legalnych" kolorów do wyboru
            nieprzypisane = [z for z in zmienne if z not in przypisanie]
            # Wykorzystujemy naszą funkcję jako kryterium porównawcze (key=lambda)
            obecna_zmienna = min(nieprzypisane,key=lambda z: len(pobierz_dozwolone_wartosci(z, przypisanie, dziedziny, ograniczenia)))

        # Zaczynamy proces testowania kolorów
        for wartosc in dziedziny[obecna_zmienna]:
            # all() upewnia się, że żaden z pokolorowanych już sąsiadów nie ma tego koloru
            if all(sasiad not in przypisanie or przypisanie[sasiad] != wartosc for sasiad in
                   ograniczenia[obecna_zmienna]):

                # Ryzykujemy i malujemy węzeł tym kolorem
                przypisanie[obecna_zmienna] = wartosc

                # Wywołujemy rekurencyjnie, aby pomalować resztę grafu
                if szukaj_rekurencyjnie(przypisanie):
                    return przypisanie  # jeżeli wykonamy całość

                # jesli wybrane kolory były złe to cofamy się o krok do tyłu
                del przypisanie[obecna_zmienna]

                # zapisujemy do kroków by wizualizacja mogła pokazać błąd
                kroki.append(copy.deepcopy(przypisanie))

        # Jeśli sprawdziliśmy wszystkie kolory i nic nie pasuje to zwracamy że dana ścieżka jest zła
        return None

    # wywołujemy algorytm z pustym słownikiem (przypisania kolorów)
    szukaj_rekurencyjnie({})

    # zwracamy dane dla wizualizacji
    return kroki, dziedziny, ograniczenia

# zadanie 1 wizualizacja
def uruchom_ui_zadanie_1(dane_csp):
    kroki_csp, pelne_dziedziny, ograniczenia = dane_csp
    pygame.init()
    ekran = pygame.display.set_mode((1100, 750))
    pygame.display.set_caption("ZADANIE 1 - Zaawansowana Wizualizacja CSP")

    kolory = {
        'TLO': (25, 25, 25),
        'TEKST': (230, 230, 230),
        'PRZYCISK': (60, 100, 150),
        'R': (200, 50, 50),
        'G': (50, 200, 50),
        'B': (50, 50, 200),
        'SZARY': (60, 60, 60),
        'WYROZNIENIE': (255, 255, 100)
    }

    font_xs = pygame.font.SysFont("Arial", 14)
    font_s = pygame.font.SysFont("Arial", 16)
    font_b = pygame.font.SysFont("Arial", 22, bold=True)
    font_znak = pygame.font.SysFont("Arial", 26, bold=True)  # Specjalny font dla symbolu "≠"

    indeks_kroku = 0
    dziala = True

    pozycje = {'X1': (550, 250), 'X2': (350, 500), 'X3': (750, 500)}

    while dziala:
        ekran.fill(kolory['TLO'])
        poz_myszy = pygame.mouse.get_pos()
        klikniecie = False

        for zdarzenie in pygame.event.get():
            if zdarzenie.type == pygame.QUIT: dziala = False
            if zdarzenie.type == pygame.MOUSEBUTTONDOWN: klikniecie = True

        ekran.blit(font_b.render("Zadanie 1: CSP z heurystyką MRV", True, kolory['TEKST']), (50, 40))
        ekran.blit(
            font_s.render("Początek to X2, a następnie wybieramy zmienną przy użyciu MRV.",
                          True, (160, 160, 160)), (50, 75))

        # --- Przycisk Dalej / Zacznij od nowa ---
        przycisk_dalej = pygame.Rect(450, 680, 200, 40)
        pygame.draw.rect(ekran, kolory['PRZYCISK'], przycisk_dalej, border_radius=5)

        if indeks_kroku < len(kroki_csp) - 1:
            tekst_przycisku = f"Krok: {indeks_kroku} / {len(kroki_csp) - 1}"
        else:
            tekst_przycisku = "Zacznij od nowa"

        ekran.blit(font_s.render(tekst_przycisku, True, kolory['TEKST']),
                   (przycisk_dalej.x + 40, przycisk_dalej.y + 10))

        # Logika zapętlania
        if klikniecie and przycisk_dalej.collidepoint(poz_myszy):
            if indeks_kroku < len(kroki_csp) - 1:
                indeks_kroku += 1
            else:
                indeks_kroku = 0  # Reset do zera

        # --- Rysowanie krawędzi i symboli "≠" ---
        krawedzie = [('X1', 'X2'), ('X1', 'X3'), ('X2', 'X3')]
        for start, koniec in krawedzie:
            punkt_start = pozycje[start]
            punkt_koniec = pozycje[koniec]
            pygame.draw.line(ekran, (120, 120, 120), punkt_start, punkt_koniec, 2)

            # Wyliczanie środka krawędzi dla symbolu nierówności z obrazka
            srodek_x = (punkt_start[0] + punkt_koniec[0]) // 2
            srodek_y = (punkt_start[1] + punkt_koniec[1]) // 2
            znak_nierownosci = font_znak.render("≠", True, (200, 200, 200))
            ekran.blit(znak_nierownosci, (srodek_x - 10, srodek_y - 15))

        obecne_przypisanie = kroki_csp[indeks_kroku]

        # --- Rysowanie węzłów ---
        for nazwa_zmiennej, pozycja in pozycje.items():
            przypisana_wartosc = obecne_przypisanie.get(nazwa_zmiennej)
            dozwolone = pobierz_dozwolone_wartosci(nazwa_zmiennej, obecne_przypisanie, pelne_dziedziny, ograniczenia)

            kolor_wezla = kolory.get(przypisana_wartosc, kolory['SZARY'])
            pygame.draw.circle(ekran, kolor_wezla, pozycja, 45)
            pygame.draw.circle(ekran, (200, 200, 200), pozycja, 45, 3)

            etykieta_nazwy = font_b.render(nazwa_zmiennej, True, (255, 255, 255))
            ekran.blit(etykieta_nazwy, (pozycja[0] - 14, pozycja[1] - 12))

            # --- Informacje obok węzła ---
            info_x = pozycja[0] + 55 if nazwa_zmiennej != 'X3' else pozycja[0] - 160
            info_y = pozycja[1] - 30

            tekst_statusu = f"Wartość: {przypisana_wartosc if przypisana_wartosc else 'Brak'}"
            ekran.blit(
                font_s.render(tekst_statusu, True, kolory['WYROZNIENIE'] if przypisana_wartosc else kolory['TEKST']),
                (info_x, info_y))

            tekst_dozwolonych = "Dostępne: " + (", ".join(dozwolone) if dozwolone else "konflikt")
            ekran.blit(font_s.render(tekst_dozwolonych, True, (100, 255, 100) if dozwolone else (255, 100, 100)),
                       (info_x, info_y + 25))

            tekst_dziedziny = f"Dziedzina: {pelne_dziedziny[nazwa_zmiennej]}"
            ekran.blit(font_xs.render(tekst_dziedziny, True, (130, 130, 130)), (info_x, info_y + 45))

        pygame.display.flip()
    pygame.quit()



# zadanie 2 logika
def oblicz_zbiory_przyblizone(dane, indeksy_atrybutow, id_zbioru_celu):
    # Słownik do grupowania obiektów o identycznych wartościach wybranych atrybutów.
    # Kluczem będzie krotka z wartościami atrybutów, a wartością lista ID obiektów.
    klasy = {}


    # Tworzenie klas nierozróżnialności
    for wiersz in dane:
        id_obiektu = wiersz[0]

        # Wycinamy z wiersza tylko te atrybuty, które nas interesują w danym zadaniu
        # (np. ignorujemy atrybut a3, jeśli funkcja otrzyma indeksy_atrybutow = [1, 2])
        wartosci_atrybutow = tuple(wiersz[i] for i in indeksy_atrybutow)

        # Jeśli taki zestaw cech pojawia się po raz pierwszy, tworzymy dla niego nową liste
        if wartosci_atrybutow not in klasy:
            klasy[wartosci_atrybutow] = []

        # Wrzucamy identyfikator obiektu do odpowiedniej listy na podstawie jego atrybutów
        klasy[wartosci_atrybutow].append(id_obiektu)

    # Przekształcamy listę obiektów docelowych na set, aby móc używać operacji takich jak .issubset()
    zbior_docelowy = set(id_zbioru_celu)

    # Wyciągamy same listy obiektów ze słownika (ignorujemy już konkretne atrybuty, bo mamy pogrupowane obiekty).
    # Funkcja sorted() jedynie porządkuje elementy (np. o1, o2), by na ekranie wyglądały estetycznie.
    lista_klas = [sorted(obiekty) for obiekty in klasy.values()]



    # przybliżenie dolne
    # Bierzemy każdy zbiór (k) z naszej listy i sprawdzamy:
    # .issubset = "Czy wszystkie elementy tego zbioru są podzbiorem zbioru docelowego?"
    # Jeśli tak, zbiór ląduje w przybliżeniu dolnym.
    dolne = [k for k in lista_klas if set(k).issubset(zbior_docelowy)]

    # przybliżenie górne
    # .isdisjoint sprawdza czy zbiory nie mają żadnych elementów wspólnych.
    # Dodając z przodu słowo 'not', szukamy tych zbiorów, które mają chociaż jeden element wspólny ze zbiorem docelowym.
    # Trafią tu automatycznie wszystkie obiekty z przybliżenia dolnego oraz obiekty sporne z obszaru granicznego.
    gorne = [k for k in lista_klas if not set(k).isdisjoint(zbior_docelowy)]


    # 3. wyniki dla UI
    # Zmienne 'dolne' i 'gorne' to teraz listy wewnątrz list (np. [['o1', 'o2'], ['o5']]).
    # tworzymy z list jedną liste [obj for sub in dolne for obj in sub] by UI mogło to dobrze przedstawić
    return {
        "klasy": lista_klas,
        "dolne": [obj for sub in dolne for obj in sub],
        "gorne": [obj for sub in gorne for obj in sub],
        "cel": id_zbioru_celu,
        "uzyte_atrybuty": indeksy_atrybutow
    }


def logika_zbiorow_przyblizonych():
    dane = [
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

    X1 = ["o1", "o2", "o3", "o7", "o9"]
    X2 = ["o5", "o6", "o8"]

    wyniki = [
        {
            "tytul": "(i) Szukamy opisu dla X2 (decyzja 'nie')",
            "podtytul": "Atrybuty: A = {a1, a2, a3}",
            "wynik": oblicz_zbiory_przyblizone(dane, [1, 2, 3], X2)
        },
        {
            "tytul": "(ii) Szukamy opisu dla X1 (decyzja 'tak')",
            "podtytul": "Atrybuty: B = {a1, a2} (pomijamy a3)",
            "wynik": oblicz_zbiory_przyblizone(dane, [1, 2], X1)
        },
        {
            "tytul": "(ii) Szukamy opisu dla X2 (decyzja 'nie')",
            "podtytul": "Atrybuty: B = {a1, a2} (pomijamy a3)",
            "wynik": oblicz_zbiory_przyblizone(dane, [1, 2], X2)
        }
    ]

    # Zwracamy gotową paczkę (surowe dane do narysowania tabeli + rozwiązane problemy)
    return {"dane": dane, "podzadania": wyniki}


# zadanie 2 wizualizacja
def uruchom_ui_zadanie_2(dane_zp):
    pygame.init()
    ekran = pygame.display.set_mode((1100, 750))
    pygame.display.set_caption("ZADANIE 2 - Wizualizacja Przybliżeń (Oznaczanie Klas)")

    surowe_dane = dane_zp['dane']
    podzadania = dane_zp['podzadania']

    kolory = {
        'TLO': (25, 25, 25),
        'TEKST': (230, 230, 230),
        'PRZYCISK': (60, 100, 150),
        'DOLNE': (40, 120, 60),  # Zielony (100% pewności)
        'GRANICA': (180, 140, 30),  # Żółto-pomarańczowy (brak pewności)
        'TLO_TABELI': (35, 35, 45),
        'ZACIEMNIENIE': (100, 100, 100)  # Kolumny wyłączone
    }

    # Paleta kontrastowych kolorów dla znaczników klas ("worków")
    kolory_klas = [(100, 200, 255), (255, 150, 100), (150, 255, 100), (255, 100, 200), (200, 150, 255), (255, 255, 100),
                   (100, 255, 200), (255, 180, 150), (200, 200, 200)]

    font_xs = pygame.font.SysFont("Arial", 12, bold=True)
    font_s = pygame.font.SysFont("Arial", 16)
    font_b = pygame.font.SysFont("Arial", 22, bold=True)
    font_tabeli = pygame.font.SysFont("Consolas", 15)

    sekwencja = [
        (0, 0), (0, 1), (0, 2),
        (1, 0), (1, 1), (1, 2),
        (2, 0), (2, 1), (2, 2)
    ]

    obecny_krok = 0
    dziala = True

    # Kolumny lekko przesunięte w prawo, aby zrobić miejsce na etykiety klas
    x_kolumn = [60, 130, 350, 480, 600]
    naglowki = ["ID", "a1", "a2", "a3", "dec"]

    opisy_faz = [
        "FAZA 1/3: Wskazanie obiektów docelowych (biała ramka).",
        "FAZA 2/3: Szukanie pewniaków - Przybliżenie Dolne (zielone).",
        "FAZA 3/3: Dodanie niepewności - Obszar Graniczny (pomarańczowe)."
    ]

    while dziala:
        ekran.fill(kolory['TLO'])
        poz_myszy = pygame.mouse.get_pos()
        klikniecie = False

        for zdarzenie in pygame.event.get():
            if zdarzenie.type == pygame.QUIT: dziala = False
            if zdarzenie.type == pygame.MOUSEBUTTONDOWN: klikniecie = True

        indeks_zadania, faza = sekwencja[obecny_krok]
        aktualne_zadanie = podzadania[indeks_zadania]
        wynik = aktualne_zadanie['wynik']

        # --- Mapowanie obiektów do ich klas (worków) ---
        mapa_klas = {}
        for id_klasy, klasa in enumerate(wynik['klasy']):
            for id_obiektu in klasa:
                mapa_klas[id_obiektu] = id_klasy

        # --- Nagłówki i Sterowanie ---
        ekran.blit(font_b.render(f"Zadanie: {aktualne_zadanie['tytul']}", True, (255, 180, 50)), (50, 30))
        ekran.blit(font_s.render(aktualne_zadanie['podtytul'], True, (180, 180, 180)), (50, 65))
        ekran.blit(font_s.render(opisy_faz[faza], True, (150, 255, 150)), (50, 95))

        przycisk_dalej = pygame.Rect(450, 680, 280, 40)
        pygame.draw.rect(ekran, kolory['PRZYCISK'], przycisk_dalej, border_radius=5)

        tekst_przycisku = f"Następny Krok ({obecny_krok + 1}/{len(sekwencja)})"
        if obecny_krok == len(sekwencja) - 1:
            tekst_przycisku = "Zacznij od nowa"

        ekran.blit(font_s.render(tekst_przycisku, True, kolory['TEKST']),
                   (przycisk_dalej.x + 30, przycisk_dalej.y + 10))

        if klikniecie and przycisk_dalej.collidepoint(poz_myszy):
            obecny_krok = (obecny_krok + 1) % len(sekwencja)

        # --- Rysowanie Tabeli ---
        y_start_tabeli = 140

        # Nagłówki
        pygame.draw.rect(ekran, (50, 50, 70), (50, y_start_tabeli, 640, 30), border_radius=4)
        for i, naglowek in enumerate(naglowki):
            kolor_naglowka = (255, 255, 255)
            if i in [1, 2, 3] and i not in wynik['uzyte_atrybuty']:
                kolor_naglowka = kolory['ZACIEMNIENIE']
            ekran.blit(font_b.render(naglowek, True, kolor_naglowka), (x_kolumn[i], y_start_tabeli + 3))

        # Wiersze (oryginalna kolejność, bez sortowania)
        for i, wiersz in enumerate(surowe_dane):
            id_obiektu = wiersz[0]
            y = y_start_tabeli + 40 + (i * 35)

            tlo_wiersza = kolory['TLO_TABELI']
            kolor_tekstu = kolory['TEKST']
            obramowanie = None

            # Renderowanie tła zależnie od obecnej fazy
            if faza >= 1 and id_obiektu in wynik['dolne']:
                tlo_wiersza = kolory['DOLNE']
                kolor_tekstu = (255, 255, 255)
            elif faza >= 2 and id_obiektu in wynik['gorne']:
                tlo_wiersza = kolory['GRANICA']
                kolor_tekstu = (255, 255, 255)

            if id_obiektu in wynik['cel']:
                obramowanie = (255, 255, 255)

            pygame.draw.rect(ekran, tlo_wiersza, (50, y, 640, 30), border_radius=4)
            if obramowanie:
                pygame.draw.rect(ekran, obramowanie, (50, y, 640, 30), width=1, border_radius=4)

            # Wartości w komórkach
            for j, wartosc in enumerate(wiersz):
                k_tekstu = kolor_tekstu
                if j in [1, 2, 3] and j not in wynik['uzyte_atrybuty']:
                    k_tekstu = kolory['ZACIEMNIENIE']
                ekran.blit(font_tabeli.render(str(wartosc), True, k_tekstu), (x_kolumn[j], y + 6))

            # --- Rysowanie Etykiety Klasy (Worka) ---
            id_klasy = mapa_klas[id_obiektu]
            kolor_klasy = kolory_klas[id_klasy % len(kolory_klas)]

            # Kolorowy prostokąt z lewej strony
            pygame.draw.rect(ekran, kolor_klasy, (20, y + 4, 25, 22), border_radius=3)
            etykieta_klasy = font_xs.render(f"K{id_klasy + 1}", True, (20, 20, 20))
            ekran.blit(etykieta_klasy, (24, y + 7))

        # --- Legenda ---
        x_legenda = 730
        ekran.blit(font_b.render("Legenda:", True, kolory['TEKST']), (x_legenda, 140))

        pygame.draw.rect(ekran, kolory['DOLNE'], (x_legenda, 180, 20, 20), border_radius=3)
        ekran.blit(font_s.render("Przybliżenie Dolne", True, kolory['TEKST']), (x_legenda + 30, 180))

        pygame.draw.rect(ekran, kolory['GRANICA'], (x_legenda, 220, 20, 20), border_radius=3)
        ekran.blit(font_s.render("Obszar Graniczny", True, kolory['TEKST']), (x_legenda + 30, 220))

        pygame.draw.rect(ekran, (255, 255, 255), (x_legenda, 260, 20, 20), width=1, border_radius=3)
        ekran.blit(font_s.render("Biała ramka (szukany cel)", True, kolory['TEKST']), (x_legenda + 30, 260))

        # Legenda znaczników
        pygame.draw.rect(ekran, kolory_klas[0], (x_legenda, 300, 25, 22), border_radius=3)
        ekran.blit(font_s.render("Znacznik 'worka' (K1, K2...)", True, kolory['TEKST']), (x_legenda + 35, 300))
        ekran.blit(font_xs.render("(Obiekty o identycznych atrybutach)", True, (150, 150, 150)), (x_legenda + 35, 322))

        pygame.display.flip()
    pygame.quit()


from itertools import combinations


# zadanie 3 logika
def logika_pokrywania_sekwencyjnego():

    dane = [
        ("o1", 1, 1, 1, 1, 3, 1, 1),
        ("o2", 1, 1, 1, 1, 3, 2, 1),
        ("o3", 1, 1, 1, 3, 2, 1, 0),
        ("o4", 1, 1, 1, 3, 3, 2, 1),
        ("o5", 1, 1, 2, 1, 2, 1, 0),
        ("o6", 1, 1, 2, 1, 2, 2, 1),
        ("o7", 1, 1, 2, 2, 3, 1, 0),
        ("o8", 1, 1, 2, 2, 4, 1, 1)
    ]

    # sey do którego będziemy wrzucać id wykreślonych obiektów (np. "o2", "o4").
    pokryte = set()

    # kroki dla UI
    kroki = []


    # z każdym krokiem reguła będzie dłuższa o 1
    for k in range(1, 7):
        #  Wybór obiektu bazowego. Bierzemy po kolei każdy wiersz z tabeli.
        for obiekt in dane:
            # Jeśli obiekt został już wykreślony, nie tworzymy z niego nowych reguł.
            if obiekt[0] in pokryte:
                continue
            # tworzymy wszystkie możliwe kombinacje atrybutów
            # np. dla k=2 wylosuje (1, 2), (1, 3) aż do (5,6)
            for kombinacja in combinations(range(1, 7), k):

                # zakłądamy że reguła jest poprawna
                czy_spojne = True
                decyzja_docelowa = obiekt[-1]  # Zapisujemy, do jakiej decyzji dążymy

                # weryfikacja niesprzeczności
                # Sprawdzamy regułe wobec wszystkich wierszy w tabeli
                for wiersz in dane:
                    # all() sprawdza, czy wszystkie wylosowane atrybuty w badanym wierszu są identyczne z atrybutami naszego obiektu bazowego
                    pasuje = all(wiersz[i] == obiekt[i] for i in kombinacja)

                    # jeżeli atrybuty są takie same ale inna jest decyzja to jest sprzeczności
                    if pasuje and wiersz[-1] != decyzja_docelowa:
                        czy_spojne = False
                        break  # przerwyamy działanie, zła reguła

                # zapisywanie reguł i wyświetlanie w UI
                # Jeśli po sprawdzeniu całej tabeli reguła jest spójna
                if czy_spojne:

                    # tworzymy zapis warunku reguły
                    warunek_reguly = " ^ ".join([f"a{i}={obiekt[i]}" for i in kombinacja])

                    nowo_pokryte = []
                    wsparcie = 0  # Licznik obiektów, które zgadzają się z regułą

                    # szukamy obiektów które wspierają tą regułe
                    for wiersz in dane:
                        if all(wiersz[i] == obiekt[i] for i in kombinacja) and wiersz[-1] == decyzja_docelowa:

                            # Zwiększamy wsparcie
                            wsparcie += 1

                            # wyrzucamy z tabeli wiersze które wspierają regułe
                            if wiersz[0] not in pokryte:
                                nowo_pokryte.append(wiersz[0])
                                pokryte.add(wiersz[0])  # Dodajemy do  zbioru wykreślonych

                    # Budujemy ostateczny tekst reguły z ilością wsparcia
                    tekst_reguly = f"({warunek_reguly}) => (d={decyzja_docelowa}) [{wsparcie}]"

                    # tworzymy krok dla UI
                    kroki.append({
                        'rzad': k,
                        'obiekt_bazowy': obiekt[0],
                        'tekst_reguly': tekst_reguly,
                        'nowo_pokryte': nowo_pokryte,
                        'wszystkie_pokryte': list(pokryte),
                        'decyzja': decyzja_docelowa
                    })
                    # wychodzimy z pętli by nie tworzyć bardziej skomplikowanych reguł
                    break

        # jeśli wykreslymy każdy wiersz, algorytm kończy pracę
        if len(pokryte) == len(dane):
            break

    # Zwracamy dane dla wizualizacji
    return dane, kroki
# zadanie 3 wizualizacja
def uruchom_ui_zadanie_3(dane_ps):
    surowe_dane, kroki = dane_ps

    pygame.init()
    ekran = pygame.display.set_mode((1250, 750))
    pygame.display.set_caption("ZADANIE 3 - Odkrywanie Reguł (Sequential Covering)")

    kolory = {
        'TLO': (25, 25, 25),
        'TEKST': (230, 230, 230),
        'PRZYCISK': (60, 100, 150),
        'ZACIEMNIENIE': (80, 80, 80),
        'WYROZNIENIE_1': (40, 120, 60),
        'WYROZNIENIE_0': (150, 50, 50),
        'TLO_TABELI': (35, 35, 45)
    }

    font_s = pygame.font.SysFont("Arial", 14)
    font_m = pygame.font.SysFont("Arial", 16)
    font_b = pygame.font.SysFont("Arial", 22, bold=True)
    font_tabeli = pygame.font.SysFont("Consolas", 15)

    indeks_kroku = 0
    dziala = True

    x_kolumn = [40, 100, 160, 220, 280, 340, 400, 460]
    naglowki = ["ID", "a1", "a2", "a3", "a4", "a5", "a6", "d"]

    while dziala:
        ekran.fill(kolory['TLO'])
        poz_myszy = pygame.mouse.get_pos()
        klikniecie = False

        for zdarzenie in pygame.event.get():
            if zdarzenie.type == pygame.QUIT: dziala = False
            if zdarzenie.type == pygame.MOUSEBUTTONDOWN: klikniecie = True

        ekran.blit(font_b.render("Zadanie 3: Idea Algorytmu Pokrywającego", True, (255, 180, 50)), (40, 30))
        ekran.blit(
            font_s.render("Zgodnie ze screenem, wykreślane obiekty (na szaro) nadal wspierają nowe reguły.", True,
                          (170, 170, 170)), (40, 60))

        # --- Przycisk "Następny krok" / "Zacznij od nowa" ---
        przycisk_dalej = pygame.Rect(450, 680, 250, 40)
        pygame.draw.rect(ekran, kolory['PRZYCISK'], przycisk_dalej, border_radius=5)

        if indeks_kroku < len(kroki):
            tekst_przycisku = f"Odkryj regułę {indeks_kroku + 1}/{len(kroki)}"
        else:
            tekst_przycisku = "Zacznij od nowa"  # Tekst po zakończeniu

        ekran.blit(font_m.render(tekst_przycisku, True, kolory['TEKST']),
                   (przycisk_dalej.x + 30, przycisk_dalej.y + 10))

        # Zmieniona logika kliknięcia (zapętlanie)
        if klikniecie and przycisk_dalej.collidepoint(poz_myszy):
            if indeks_kroku < len(kroki):
                indeks_kroku += 1
            else:
                indeks_kroku = 0  # Reset do zera

        obecny_krok = kroki[indeks_kroku - 1] if indeks_kroku > 0 else None
        wczesniej_pokryte = kroki[indeks_kroku - 2]['wszystkie_pokryte'] if indeks_kroku > 1 else []
        nowo_pokryte = obecny_krok['nowo_pokryte'] if obecny_krok else []

        # --- Rysowanie Tabeli (Lewa strona) ---
        y_start_tabeli = 120
        pygame.draw.rect(ekran, (50, 50, 70), (30, y_start_tabeli, 480, 30), border_radius=4)
        for i, naglowek in enumerate(naglowki):
            ekran.blit(font_b.render(naglowek, True, (255, 255, 255)), (x_kolumn[i], y_start_tabeli + 3))

        for i, wiersz in enumerate(surowe_dane):
            id_obiektu = wiersz[0]
            y = y_start_tabeli + 40 + (i * 35)

            tlo_wiersza = kolory['TLO_TABELI']
            kolor_tekstu = kolory['TEKST']

            if id_obiektu in wczesniej_pokryte:
                tlo_wiersza = kolory['TLO']
                kolor_tekstu = kolory['ZACIEMNIENIE']
            elif id_obiektu in nowo_pokryte:
                tlo_wiersza = kolory['WYROZNIENIE_1'] if obecny_krok['decyzja'] == 1 else kolory['WYROZNIENIE_0']
                kolor_tekstu = (255, 255, 255)

            pygame.draw.rect(ekran, tlo_wiersza, (30, y, 480, 30), border_radius=4)
            if id_obiektu in nowo_pokryte:
                pygame.draw.rect(ekran, (255, 255, 255), (30, y, 480, 30), width=1, border_radius=4)

            for j, wartosc in enumerate(wiersz):
                ekran.blit(font_tabeli.render(str(wartosc), True, kolor_tekstu), (x_kolumn[j], y + 6))

        # --- Rysowanie Wygenerowanych Reguł (Prawa strona) ---
        x_start_reguly = 550
        ekran.blit(font_b.render("Wygenerowane Reguły (Zgodne z obrazkiem):", True, kolory['TEKST']),
                   (x_start_reguly, 120))

        for i in range(indeks_kroku):
            krok = kroki[i]
            ry = 160 + (i * 60)

            czy_aktywna = (i == indeks_kroku - 1)
            kolor_tla = (60, 65, 80) if czy_aktywna else (40, 45, 60)
            pygame.draw.rect(ekran, kolor_tla, (x_start_reguly, ry, 650, 50), border_radius=5)
            if czy_aktywna:
                pygame.draw.rect(ekran, (200, 200, 200), (x_start_reguly, ry, 650, 50), width=2, border_radius=5)

            kolor_decyzji = (150, 255, 150) if krok['decyzja'] == 1 else (255, 150, 150)

            naglowek_reguly = f"Rząd-{krok['rzad']}: {krok['obiekt_bazowy']} => {krok['tekst_reguly']}"
            ekran.blit(font_m.render(naglowek_reguly, True, kolor_decyzji), (x_start_reguly + 10, ry + 8))

            tekst_pokrycia = f"Wyrzuca z rozważań: {', '.join(krok['nowo_pokryte'])}"
            ekran.blit(font_s.render(tekst_pokrycia, True, (180, 180, 180)), (x_start_reguly + 10, ry + 28))

        pygame.display.flip()
    pygame.quit()

# ==================================================================================
# PANEL GŁÓWNY (WYBÓR MODUŁU DO URUCHOMIENIA)
# ==================================================================================
if __name__ == "__main__":
    print("\n--- SYSTEMY DECYZYJNE - MENU ---")
    print("Obliczanie logiki w tle...")

    # Wywołanie funkcji logicznych niezależnie od renderowania
    dane_zad_1 = logika_csp()
    dane_zad_2 = logika_zbiorow_przyblizonych()
    dane_zad_3 = logika_pokrywania_sekwencyjnego()

    while True:
        print("\nzadania: ")
        print("1. Zadanie 1: CSP")
        print("2. Zadanie 2: Zbiory Przybliżone")
        print("3. Zadanie 3: Reguły Sekwencyjne")
        print("0. Wyjście")

        wybor = input("Twój wybór: ")

        if wybor == '1':
            uruchom_ui_zadanie_1(dane_zad_1)
        elif wybor == '2':
            uruchom_ui_zadanie_2(dane_zad_2)
        elif wybor == '3':
            uruchom_ui_zadanie_3(dane_zad_3)
        elif wybor == '0':
            print("Koniec programu.")
            break
        else:
            print("Nieprawidłowy wybór.")