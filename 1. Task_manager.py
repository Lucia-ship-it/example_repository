# ZADANIE OBECNE
# Každá funkce má svůj specifický úkol
# Úkoly budou ukládány do seznamu ukoly = []



#ZADANIE 1 - def pridat_ukol():
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

# zadanie 2 - zobrazeni ukolu
# ok    zobrazi vsechny ukoly v seznamu
# ok    pak zobrazeni hlavniho menu
# ok    platí volba 2 v hlavním menu

def zobrazit_ukoly():
    print(vsechny_ukoly)
    print("\n\n")
    hlavni_menu()

#zadanie 3 - odstranit ukol
# ok    umožnit zadat číslo úkolu, který chce odstranit
# ok    platí volba 3 v hlavním menu
# ok    je potřeba, aby uživatel viděl všechny uložené úkoly
#při výběru neexistujícího úkolu byl upozorněn.
#program pokračuje dál nabídkou hlavního menu

# UPRAVENY NADEJNY KOD: osetrit neciselne vstupy...:/

# zoznam = ["jablko","hruska","kiwi","melon"]
# print(zoznam)

# #enumetare priradi k polozkam zoznamu cislo

# for i, uloha in enumerate(zoznam, start=1):
#     print(f"{i}. {uloha}")

# while True:
#     vyber_cisla = int(input("Zadej číslo úkolu, který chceš smazat"))

#     index_cisla=vyber_cisla - 1
#     print(zoznam[index_cisla])

#     if 0 <= index_cisla < len(zoznam):
#         odstraneny_index = zoznam.pop(index_cisla)
#         print(f"Úkol číslo {vyber_cisla} byl smazán")
#         print(f"Smazali jste: {odstraneny_index}.")
#         break
#     else:
#         print(f"V zozname sa nenachází úkol číslo {vyber_cisla}. Vyber číslo ze seznamu.")
        
# print(zoznam)

# hlavni_menu()    

#volba 4 v hlavnim menu
#program se ukončí

def konec_programu():
    print("\nKonec programu.")


# zadanie 0 - Funkce hlavního menu
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
            odstraneni_ukolu()
            break
        elif vyber_cisla == 4:
            konec_programu()
            print("Naviděnou!")
            exit()
        else:
            vyber_cisla=int(input("Vyberte možnost (1-4):"))
            print(vyber_cisla)

hlavni_menu()

