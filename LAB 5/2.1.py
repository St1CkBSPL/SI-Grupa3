def perceptron_x1_and_not_x2(x1, x2):
    # Wagi perceptronu
    w0 = -0.5
    w1 = 1.0
    w2 = -1.0
    
    # Obliczenie sumy 
    suma = w0 + (w1 * x1) + (w2 * x2)
    
    if suma > 0:
        return 1
    else:
        return 0

# Testowanie perceptronu dla wszystkich kombinacji
dane_testowe = [
    (0, 0),
    (0, 1),
    (1, 0),
    (1, 1)
]

print("x1 | x2 | Oczekiwane | Wynik perceptronu")
print("-" * 40)
for x1, x2 in dane_testowe:
    # Obliczenie oczekiwanej wartości x1 AND (NOT x2)
    oczekiwane = 1 if (x1 == 1 and x2 == 0) else 0
    wynik = perceptron_x1_and_not_x2(x1, x2)
    
    print(f" {x1} |  {x2} |      {oczekiwane}     |        {wynik}")