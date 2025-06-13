# ZADANIE
# Každá funkce má svůj specifický úkol
# Úkoly budou ukládány do seznamu ukoly = []



#UKOL 2 - def pridat_ukol():
# ok    volba 1 v hlavním menu
# ok    nazev a popis noveho ukolu
# ok    ulozit do zoznamu
# ok    zobrazit nabidku hlavneho menu
#!!!! osetrit zadanie prazdneho vstupu

vsechny_ukoly = []
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
        "popis úkolu" : popis
        }
    vsechny_ukoly.append(novy_ukol)
    print(f"Úkol {nazev} byl přidán.\n")

#zadanie 1
# UKOL 1 - Funkce hlavního menu
# přidání, zobrazení a odstranění úkolu. 
# neplatnou volbu, program ho upozorní a nechá uživatele opakovat znovu volbu.

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
            pridat_ukol()
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



