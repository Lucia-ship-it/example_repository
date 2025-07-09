#rozsirena funkcia pre zadanie vsetkých vstupov pri aktualizácií úlohy. Na konci možné odsúhlasiť, znovu zadať alebo vrátiť sa do menu. spustenie mozne pri inplementácii do zakladného kódu

def aktualizace_ukolu(conn):
    print("\nSeznam úkolů:")
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(
        "SELECT * FROM Ukoly;"
                )
    vsechny_ukoly_vyber = cursor.fetchall()
    for ukol_vyber in vsechny_ukoly_vyber:
        print(ukol_vyber)
    
    # Vybere úkol podle ID.
    while True:
        vyber_ukolu_id = int(input("\nZadejte ID úkolu, který chcete upravit: "))
        if vyber_ukolu_id in vsechny_ukoly_vyber[0]:
            print(f"K úpravě jste vybrali úlohu s id {vyber_ukolu_id}.")
            cursor.execute(
                "SELECT id, nazev, popis, stav FROM Ukoly WHERE id=%s;",vyber_ukolu_id
            )
            ukazka_ukolu = cursor.fetchone()
            print(ukazka_ukolu)
        else:
            print("\nZadejte správnou hodnotu id.")
            
                                
        while True:  #osetrenie prazdneho vstupu
            print("\n\nZadejte, jak má aktualizovaný řádek vypadat: ")
            nazev = input("Zadejte nový název úkolu: ").strip()
            if nazev == "":
                print("\nVyplnění je povinné\n")
            else:
                break
            

        while True:
            popis = input("Zadejte nový popis úkolu: ").strip()
            if popis == "":
                print("\nVyplnění je povinné\n")
            else:
                break

        while True:
            print("Zadejte stav úkolu výběrem z možností:'Nezahájeno', 'Probíhá', 'Hotovo'" )
            hodnoty_stavu = ['Nezahájeno', 'Probíhá', 'Hotovo']
            stav = input("Vyplnte nový stav: ").strip()

            if stav == "":
                print("\nVyplnění je povinné\n")
            elif stav not in hodnoty_stavu:
                print("\nZadej stav z uvedených možností.\n")
            else:
                break


            #Po potvrzení se aktualizuje DB.
        while True:
            print(f"\nChcete uložit takhle upravený záznam? 'Název úkolu: {nazev}, popis úkolu: {popis}, stav úkolu: {stav}'?\n")
            potvrdenie = input("Napšte 'ano' nebo 'ne': ")

            if potvrdenie == "":
                print("\nVyplnění je povinné\n")
            elif potvrdenie == 'ne':
                print("❌ Aktualizace byla zrušena.")
                break
            elif potvrdenie == 'menu':
                print("Budete přesměrovaný na hlavní menu.")
                return
            elif potvrdenie == 'ano':
                cursor.execute(
                    "UPDATE Ukoly SET nazev = %s, popis = %s, stav = %s WHERE id = %s;", 
                    (nazev, popis, stav, vyber_ukolu_id)
                    )
                conn.commit()
                print("✅ Úkol byl úspěšně aktualizován.")
                return
            else:
                print("Prosím zadejte požadovaný výraz. Jestli si přejete přejít na Hlavní menu, napište 'menu'.")