# ZADANIE OBECNE
# Každá funkce má svůj specifický úkol
# Úkoly budou ukládány do seznamu ukoly = []



#ZADANIE 2 - def pridat_ukol():
# ok    volba 1 v hlavním menu
# ok    nazev a popis noveho ukolu
# ok    ulozit do zoznamu
# ok    zobrazit nabidku hlavneho menu
#!!!! osetrit zadanie prazdneho vstupu

vsechny_ukoly = [
    {
        "nazev" : "priklad_1",
        "popis" : "popis_1"
     },
    {
        "nazev" : "priklad_2",
        "popis" : "priklad_2"
    }
]

def pridat_ukol():
    while True:
        nazev = input("\nZadejte název úkolu:").strip()
        if nazev == "":
            print("Vyplnenie je povinné")
        else:
            break

    while True:
        popis = input("Zadejte popis úkolu:").strip()
        if popis == "":
            print("Vyplnenie je povinné")
        else:
            break



    novy_ukol = {
        "název" : nazev,
        "popis" : popis
        }
    vsechny_ukoly.append(novy_ukol)
    print(f"Úkol {nazev} byl přidán.\n")

# zadanie 3 - zobrazeni ukolu
# ok    zobrazi vsechny ukoly v seznamu
# ok    pak zobrazeni hlavniho menu
# ok    platí volba 2 v hlavním menu

def zobrazit_ukoly():
    print(vsechny_ukoly)
    print("\n\n")
    hlavni_menu()

# zadanie 1 - Funkce hlavního menu
# ok    přidání, zobrazení a odstranění úkolu. 
# ok    neplatnou volbu, program ho upozorní a nechá uživatele opakovat znovu volbu.

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
            print("Přidání nového úkolu")
            pridat_ukol()
        elif vyber_cisla == 2:
            print("Zobrazení všech úkolů")
            zobrazit_ukoly()
        elif vyber_cisla == 3:
            print("Odstranění úkolu")
            break
        elif vyber_cisla == 4:
            print("Naviděnou")
            break
        else:
            vyber_cisla=int(input("Vyberte možnost (1-4):"))
            print(vyber_cisla)

hlavni_menu()

