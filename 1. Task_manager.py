def hlavni_menu():
    print("Správce úkolů - Hlavní menu")
    print("1. Přidat nový úkol")
    print("2. Zobrazit všechny úkoly")
    print("3. Odstranit úkol")
    print("4. Konec programu")
    
    while True:
        vyber_cisla=int(input("Vyberte možnost (1-4):"))
        print(vyber_cisla)
        if vyber_cisla == 1:
            print("Volba cislo 1")
            break
        elif vyber_cisla == 2:
            print("Volba cislo 2")
            break
        elif vyber_cisla == 3:
            print("Volba cislo 3")
            break
        elif vyber_cisla == 4:
            print("Volba cislo 4")
            break
        else:
            vyber_cisla=int(input("Vyberte možnost (1-4):"))
            print(vyber_cisla)

hlavni_menu()