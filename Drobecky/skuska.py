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


# def odstranit_ukol():  
#     print("\nZobrazení všech úkolů:")

#     for i, uloha in enumerate(vsechny_ukoly, start=1):
#         print(f"{i}.{uloha}")

# #     while True:
# #         try:
# #             vyber_cisla = int(input("\nZadejte číslo úkolu, který chcete smazat: \n"))
# #             index_cisla = vyber_cisla - 1 
        
# #             if 0 < index_cisla <= len(vsechny_ukoly):
# #                 odstraneny_index = vsechny_ukoly.pop(index_cisla) 
                
# #                 print(f"Úkol číslo {vyber_cisla} byl smazán")
# #                 print(f"Smazali jste: {odstraneny_index}.\n")
# #                 #break
# #             else:
# #                 print(f"V zozname sa nenachází úkol číslo {vyber_cisla}. Vyber číslo ze seznamu.")
# #         except ValueError:
# #             print("Zadej číselný vstup!")

# #     while True:
# #        if not vsechny_ukoly:
# #             print("Zoznam úkolů je prázdný. Budete přesměrovány do hlavního menu.")
            
# # odstranit_ukol()    

# def odstranit_ukol():
#     print("\nZobrazení všech úkolů:")
#     for i, uloha in enumerate(vsechny_ukoly, start=1):
#         print(f"{i}.{uloha}")

#     while len(vsechny_ukoly) > 0:
#         try:
#             vyber_cisla = int(input("\nZadejte číslo úkolu, který chcete smazat: \n"))
#             index_cisla = vyber_cisla - 1 

        
#             if 0 <= index_cisla < len(vsechny_ukoly):
#                 odstraneny_index = vsechny_ukoly.pop(index_cisla) 
                
#                 print(f"Úkol číslo {vyber_cisla} byl smazán")
#                 print(f"Smazali jste: {odstraneny_index}.\n")
#                 # break
#             else:
#                 print(f"\nV zozname sa nenachází úkol číslo {vyber_cisla}. Vyber číslo ze seznamu.")
#         except ValueError:
#             print("Zadej číselný vstup!")
    
#     print("Zoznam je prázny, budete presmerovaný na hlavne menu\n")       
#     hlavni_menu()    

def odstranit_ukol():
    if len(vsechny_ukoly) == 0:
        print("Zoznam je prázny, budete presmerovaný na hlavne menu\n")  
        return
    else:
        print("\nZobrazení všech úkolů:")
        for i, uloha in enumerate(vsechny_ukoly, start=1):
            print(f"{i}.{uloha}")
    
        while vsechny_ukoly:
            try:
                vyber_cisla = int(input("\nZadejte číslo úkolu, který chcete smazat: \n"))
                index_cisla = vyber_cisla - 1 
            
                if 0 <= index_cisla < len(vsechny_ukoly):
                    odstraneny_index = vsechny_ukoly.pop(index_cisla) 
                    
                    print(f"Úkol číslo {vyber_cisla} byl smazán")
                    print(f"Smazali jste: {odstraneny_index}.\n")
                    return
                else:
                    print(f"\nV zozname sa nenachází úkol číslo {vyber_cisla}. Vyber číslo ze seznamu.")
            except ValueError:
                print("Zadej číselný vstup!")

odstranit_ukol()