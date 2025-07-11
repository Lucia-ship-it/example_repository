import pymysql
from datetime import date

# 2. vytvoreni_tabulky() – Vytvoření tabulky, pokud neexistuje
# OK OK - Funkce vytvoří tabulku ukoly, pokud ještě neexistuje. create_table_if_not_exist(conn)
#  - Ověří existenci tabulky v databázi.

def create_table_if_not_exist(conn): #slo by na test
    cursor = conn.cursor()
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Ukoly_test (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nazev VARCHAR (50) NOT NULL,
            popis VARCHAR (255) NOT NULL,
            stav  ENUM ('Nezahájeno', 'Probíhá', 'Hotovo') NOT NULL DEFAULT 'Nezahájeno', 
            datum_vytvoreni DATE DEFAULT (CURRENT_DATE)
            );
        ''')
        print("✅ Tabulka 'Ukoly_test' je vytvořena.")
        conn.commit()
    except pymysql.MySQLError as err:
        print(f"Chyba při vytváření tabulky: {err}")
    finally:
        cursor.close()

# ---------- Funkce programu ----------
# 1. pripojeni_db() – Připojení k databázi
# OK OK Funkce vytvoří připojení k MySQL databázi. connect_to_db()
# OK Pokud připojení selže, zobrazí chybovou zprávu.


def connect_to_db(): #slo by na test
    try:
        conn = pymysql.connect(
                host="mysql80.r4.websupport.sk",
                port=3314,
                user="EsPMMROq",
                password="79_|rBg[1F=`}cj|I%kc",
                database="Task_manager_SQL"            
            )
        print("\nPřipojení k databázi bylo úspěšné. Databáze Task_manager_SQL je k dispozici.")
        
        create_table_if_not_exist(conn)
        return conn
    except pymysql.MySQLError as err:
        print(f"❌ Chyba při připojování: {err}")



# 3. hlavni_menu() – Hlavní nabídka - def main()
# OK OK  Zobrazí možnosti menu:
# OK OK Pokud uživatel zadá špatnou volbu, program ho upozorní a nechá ho vybrat znovu.

def main(): #k testu
    try:
        conn = connect_to_db()
    except pymysql.MySQLError as err:
        print(f"❌ Nelze navázat spojení s databází v main: {err}")
        return
    
    while True:
        print("\nSprávce úkolů - Hlavní menu")
        print("1. Přidat úkol")
        print("2. Zobrazit všechny úkoly")
        print("3. Aktualizovat stav úkolu")
        print("4. Odstranit úkol")
        print("5. Ukončit program")

        vyber_cisla=(input("Vyberte možnost (1-5):"))
                 
        if vyber_cisla == "1":
            print("\nPřidání nového úkolu")
            pridat_ukol_sql(conn)
        elif vyber_cisla == "2":
            print("\nZobrazení všech úkolů:")
            get_all_tasks(conn)
        elif vyber_cisla == "3":
            print("\nVolba Aktualizovat stav úkolu:")
            aktualizace_ukolu(conn)
        elif vyber_cisla == "4":
            print("\nVolba Odstranění úkolu:")
            odstraneni_ukolu(conn)
        elif vyber_cisla == "5":
            print("\nKonec programu, naschledanou.👋\n")
            exit()
        else:
            print("\nZadejte správnou volbu menu.")

        conn.close()

# 4. pridat_ukol() – Přidání úkolu
#  Uživatel zadá název a popis úkolu.
# OK     Povinné údaje: Název a popis jsou povinné, nesmí být prázdné.
# OK     Automatické hodnoty:
# OK    1. Úkol dostane ID automaticky.
# OK    2. Výchozí stav ukolu: Nezahájeno
# OK OK Po splnění všech podmínek se úkol uloží do databáze - def pridat_ukol_sql(conn,nazev_ukolu, popis_ukolu)

def pridat_ukol_sql(conn,nazev_ukolu, popis_ukolu):
    pridat_ukol_vstupy(conn)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Ukoly_test (nazev, popis) VALUES (%s,%s);", 
        (nazev_ukolu, popis_ukolu)
        )
    conn.commit()
    cursor.close()

def pridat_ukol_vstupy(conn, nazev: str, popis: str) -> str:
    nazev = nazev.strip()
    popis = popis.strip()
    if not nazev or not popis:
        return ""
    return f"{nazev}: {popis}"  


# 5. zobrazit_ukoly() – Zobrazení úkolů
#  OK OK Seznam všech úkolů s informacemi: ID, název, popis, stav. -> def get_all_tasks(conn)
#  OK OK Filtr: Zobrazí pouze úkoly se stavem "Nezahájeno" nebo "Probíhá". -> def data_filter(conn)
#  Pokud nejsou žádné úkoly, zobrazí informaci, že seznam je prázdný.


def get_all_tasks(conn):
    print("\nSeznam všech úkolů:") 
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT id, nazev, popis, stav FROM Ukoly_test;"
        )
        all_tasks = cursor.fetchall()
        return all_tasks
    except pymysql.MySQLError as err:
        print(f"❌ Chyba při načítání úkolů: {err}")
        #return []
    finally:
        cursor.close()

 

def data_filter(conn):# k testu 
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute(
            "SELECT id, nazev, popis, stav FROM Ukoly_test WHERE stav IN ('Nezahájeno', 'Probíhá');"
        )
        nedokoncene_ukoly = cursor.fetchall()
        return nedokoncene_ukoly
    finally:
        cursor.close()

# def data_filter_input(conn): #PROBLEM S INPUTMI
#     vyber_filtru = input("\nChcete vyfiltrovat pouze Nedokončené úkoly? Napište 'ano' nebo 'ne': ").strip()      
#     if vyber_filtru == 'ano':
#         print("\nZobrazení nedokončených úkolů: ")
#         vysledky_filtru = data_filter(conn)        
#         for vysledky in vyber_filtru:
#             print(vysledky)
#     elif vyber_filtru == "":
#         print("\nVyplnění je povinné")
#     else:
#         print("Budete přesměrováni do hlavního menu.")
        

# 6. aktualizovat_ukol() – Změna stavu úkolu
# OK OK     Uživatel vidí seznam úkolů (ID, název, stav). -> get_all_tasks(conn)
# OK OK     Vybere úkol podle ID. -> def get_task_id(conn,vyber_id)
# OK OK     Dostane na výběr nový stav: "Probíhá" nebo "Hotovo"
# OK OK     Po potvrzení se aktualizuje DB. -> def update_tast_status(conn, vyber_id, novy_stav):
# OK Pokud zadá neexistující ID, program ho upozorní a nechá ho vybrat znovu.
def aktualizace_ukolu(conn,id):
    get_all_tasks(conn)
    get_task_id(conn,id)
    

      
#vstav dat do formatu na vyber cisla, aby to nemusel s diakritikou vyplnat. podobne ako vyber 

def update_tast_status(conn, vyber_id, novy_stav):
    povolene_stavy = ['Probíhá', 'Hotovo']
    if novy_stav not in povolene_stavy:
        raise ValueError("Neplatný stav úkolu")
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Ukoly_test SET stav = %s WHERE id = %s;", 
            (novy_stav, vyber_id)
        )
        conn.commit()
        ukol_update =cursor.fetchone()
        print("✅ Úkol byl úspěšně aktualizován.")
        return ukol_update
    except pymysql.MySQLError as err:
        print(f"❌ Chyba při aktualizaci úkolu: {err}")
        return 0
    finally:
        cursor.close()


def get_task_id(conn,vyber_id):#pouzitie na aktualizaciu aj delete #k testu
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT id FROM Ukoly_test WHERE id=%s;",
            (vyber_id,)
        )
        vyber_id = cursor.fetchone()
        return vyber_id["id"] if vyber_id else None #Ak neexistuje (status is None)
            #raise ValueError("Zadejte spprávné id úkolu.")
    except pymysql.MySQLError as err:
        print(f"❌ Chyba při výběru id úkolu {err}")
    finally:
        cursor.close()
 
  
def kontrola_id_status(conn, vyber_id):
    id_exist = get_task_id(conn, vyber_id)
    if id_exist is None:
        raise ValueError("Zadané ID neexistuje.")
    
    
    #        
            

#             conn.commit()
#             print("\n✅ Úkol byl úspěšně aktualizován.\nNyní budete přesměrováni do hlavního menu.")
#             return
#         else:
#             print("\nZadejte správnou hodnotu pro stav")
        
    
    

# 7. odstranit_ukol() – Odstranění úkolu
# OK Uživatel vidí seznam úkolů.
# OK Vybere úkol podle ID.
# OK Po potvrzení bude úkol trvale odstraněn z databáze.
# OK Pokud uživatel zadá neexistující ID, program ho upozorní a nechá ho vybrat znovu.
def odstraneni_ukolu():    
    print("\nSeznam všech úkolů:") 
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(
        "SELECT id, nazev, popis, stav FROM Ukoly_test;"
        )
    ukoly_vsechny = cursor.fetchall()
    if len(ukoly_vsechny) == 0:
        print("Seznam úkolů je prázdný")
    for ukol in ukoly_vsechny:
        print(ukol)
    vsechna_id = [ukol['id'] for ukol in ukoly_vsechny]

    while True:
        try:
            vyber_ukolu_id = int(input("\nZadejte ID úkolu, který chcete smazat: ")) # musime osetrit ValueError, keby sa nezada cislo

            if vyber_ukolu_id in vsechna_id:
                print(f"K odstranění jste vybrali úkol s id {vyber_ukolu_id}.")
                cursor.execute(
                    "DELETE FROM Ukoly_test WHERE id=%s;",
                    (vyber_ukolu_id,)
                )
                print("Úkol byl odstraněn.")
                break
            else:
                print("\nZadejte správnou hodnotu id.")
        except ValueError:
            print("\n❗ Prosím, zadejte platné číslo.")
        except pymysql.MySQLError as err:
            print(f"❌ Chyba při výběru id úkolu {err}")

#------SPURSTENIE PROGRAMU-------

conn = connect_to_db()
if conn:
    
   