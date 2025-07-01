# ZADANIE OBECNE
# Každá funkce má svůj specifický úkol
# Úkoly budou ukládány do seznamu ukoly = []



# ok    ZADANIE 1 - def pridat_ukol():
# ok    volba 1 v hlavním menu
# ok    nazev a popis noveho ukolu
# ok    ulozit do zoznamu
# ok    zobrazit nabidku hlavneho menu
# ok    osetrit zadanie prazdneho vstupu

vsechny_ukoly = [
    {
        "nazev" : "priklad_1",
        "popis" : "popis_1"
     },
    {
        "nazev" : "priklad_2",
        "popis" : "popis_2"
    }
]

def pridat_ukol():
    while True: #osetrenie prazdneho vstupu
        nazev = input("\tZadejte název úkolu: ").strip() 
        if nazev == "":
            print("\nVyplnenie je povinné\n")
        else:
            break

    while True:
        popis = input("\tZadejte popis úkolu: ").strip()
        if popis == "":
            print("\nVyplnenie je povinné\n")
        else:
            break

    novy_ukol = {
        "název" : nazev,
        "popis" : popis
        }
    vsechny_ukoly.append(novy_ukol)
    print(f"\nÚkol '{nazev}' byl přidán.\n")

# ok    zadanie 2 - zobrazeni ukolu
# ok    zobrazi vsechny ukoly v seznamu
# ok    pak zobrazeni hlavniho menu
# ok    platí volba 2 v hlavním menu

def zobrazit_ukoly():
    for i, uloha in enumerate(vsechny_ukoly, start=1):
        print(f"{i}.{uloha}")

    print("\n\n")
    hlavni_menu()

# ok    zadanie 3 - odstranit ukol
# ok    umožnit zadat číslo úkolu, který chce odstranit
# ok    platí volba 3 v hlavním menu
# ok    je potřeba, aby uživatel viděl všechny uložené úkoly
# ok    při výběru neexistujícího úkolu byl upozorněn.
# ok    program pokračuje dál nabídkou hlavního menu

def odstranit_ukol():
    #print(vsechny_ukoly)
    for i, uloha in enumerate(vsechny_ukoly, start=1):
        print(f"{i}.{uloha}")

    while True:
        try:
            vyber_cisla = int(input("\nZadej číslo úkolu, který chceš smazat: \n"))
            index_cisla = vyber_cisla - 1 
        
            if 0 <= index_cisla <= len(vsechny_ukoly):
                odstraneny_index = vsechny_ukoly.pop(index_cisla) 
                
                print(f"Úkol číslo {vyber_cisla} byl smazán")
                print(f"Smazali jste: {odstraneny_index}.\n")
                break
            else:
                print(f"V zozname sa nenachází úkol číslo {vyber_cisla}. Vyber číslo ze seznamu.")
        except ValueError:
            print("Zadej číselný vstup!")
            
    hlavni_menu()    

# ok    zadanie 4 - konec
# ok    volba 4 v hlavnim menu
# ok    program se ukončí

# def konec_programu():
    # print("\nKonec programu.")
    # print("Naviděnou!")
    # exit()


# ok    zadanie 0 - Funkce hlavního menu
# ok    přidání, zobrazení a odstranění úkolu. 
# ok    neplatnou volbu, program ho upozorní a nechá uživatele opakovat znovu volbu.

def hlavni_menu():
    print("\nSprávce úkolů - Hlavní menu")
    print("1. Přidat nový úkol")
    print("2. Zobrazit všechny úkoly")
    print("3. Odstranit úkol")
    print("4. Konec programu")
    
    while True:
        try:
            vyber_cisla=int(input("Vyberte možnost (1-4):"))
            #print(vyber_cisla)
            if vyber_cisla ==1:
                print("\nPřidání nového úkolu")
                pridat_ukol()
            elif vyber_cisla ==2:
                print("\nZobrazení všech úkolů:")
                zobrazit_ukoly()
            elif vyber_cisla ==3:
                print("\nOdstranění úkolu")
                odstranit_ukol()
            elif vyber_cisla ==4:
                # konec_programu()
                print("\nKonec programu.\n")
                exit()
            else:
                print("\nZadejte správnou hodnotu.")
                vyber_cisla=int(input("Vyberte možnost (1-4):"))
        except ValueError:
            print("\nZadejte správnou hodnotu.")
            # vyber_cisla=int(input("Vyberte možnost (1-4):"))
            

hlavni_menu()

