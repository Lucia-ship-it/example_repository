import pymysql
from datetime import date

def vytvor_pripojeni(): 
    try:
        conn = pymysql.connect(
                host="mysql80.r4.websupport.sk",
                port=3314,
                user="EsPMMROq",
                password="79_|rBg[1F=`}cj|I%kc",
                database="Task_manager_SQL"            
            )
        print("\n✅ Připojení k databázi bylo úspěšné. Databáze Task_manager_SQL je k dispozici.")
        
        return conn
    except pymysql.MySQLError as err:
        print(f"❌ Chyba při připojování: {err}")   
        return None 
    
#-----------------OVERENIE/VYTVORENIE TABULKY---------------   
def create_table_if_not_exist(conn) -> bool:
    """
    Vytvorí tabulku Ukoly_test, ak ešte neexistuje.
    Vracia True, ak bola vytvorená alebo už existovala.
    Vracia False, ak nastala chyba.
    """
    try:
        cursor = conn.cursor()

        # Overenie, či už tabuľka existuje
        cursor.execute("SHOW TABLES LIKE 'Ukoly_test';")
        existuje = cursor.fetchone()

        if existuje:
            print("ℹ️  Tabulka 'Ukoly_test' již existuje.")
            return True

        # Ak neexistuje, vytvor ju
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Ukoly_test (
                id INT PRIMARY KEY AUTO_INCREMENT,
                nazev VARCHAR(50) NOT NULL,
                popis VARCHAR(255) NOT NULL,
                stav ENUM('Nezahájeno', 'Probíhá', 'Hotovo') NOT NULL DEFAULT 'Nezahájeno',
                datum_vytvoreni DATE DEFAULT (CURRENT_DATE)
            );
        ''')
        conn.commit()
        print("✅ Tabulka 'Ukoly_test' byla vytvořena.")
        return True

    except pymysql.MySQLError as err:
        print(f"❌ Chyba při vytváření tabulky: {err}")
        return False

    finally:
        cursor.close()

#-------------------FUNKCIA: PRIDAJ UKOL---------------
def add_task_into_sql(conn,nazev_ukolu, popis_ukolu):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Ukoly_test (nazev, popis) VALUES (%s,%s);", 
        (nazev_ukolu.strip(), popis_ukolu.strip())
        )
    conn.commit()
    cursor.close()

def add_task_overenie_input(nazev_ukolu: str, popis_ukolu: str) -> str: # -> oznacuje, ze funkccia vrati retazec. 
    nazev_ukolu = nazev_ukolu.strip()
    popis_ukolu = popis_ukolu.strip()
    if not nazev_ukolu or not popis_ukolu:
        return ""
    return f"Nazev nového úkolu: {nazev_ukolu}, popis: {popis_ukolu}"  
   
def add_task_input(conn):
    while True:
        nazev_ukolu = input("Zadejte název úkolu: ").strip()
        popis_ukolu = input("Zadejte popis úkolu: ").strip()

        vysledok = add_task_overenie_input(nazev_ukolu, popis_ukolu)

        if vysledok:
            print(f"\n✅ Úkol přidán: {vysledok}")
            add_task_into_sql(conn,nazev_ukolu, popis_ukolu)
            break
        else:
            print("\n❌ Název a popis musí být vyplněny.\nZkuste to znovu.\n")

#-------------------FUNKCIA ZOBRAZIT UKOLy-----------------

def get_all_tasks(conn):
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, nazev, popis, stav FROM Ukoly_test;")
        tasks = cursor.fetchall()  #  dá sa testovať pomocou assert
        
        if tasks:
            print("\n📋 Seznam všech úkolů:")
            for task in tasks:
                print(task)
        else:
            print("📭 Seznam úkolů je prázdný.")
        return tasks

    except pymysql.MySQLError as err:
        print(f"❌ Chyba při načítání úkolů: {err}")
        return []
    finally:
        cursor.close()

def data_filter(conn):
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT id, nazev, popis, stav FROM Ukoly_test WHERE stav IN ('Nezahájeno', 'Probíhá');"
        )
        return cursor.fetchall()
    finally:
        cursor.close()



#-------------------FUNCIA AKTUALIZACIA UKOLU----------------
def zmen_stav_ukolu_input(conn):
    tasks = get_all_tasks(conn)
    if not tasks:
        print("Není co aktualizovat.\n")
        return

    while True:
        try:
            vyber_id = int(input("\nZadejte ID úkolu, jehož stav chcete změnit: "))
            if not kontrola_id_status(conn, vyber_id):
                print("❌ Zadané ID neexistuje. Zkuste znovu.")
                continue
            break
        except ValueError:
            print("❌ Zadejte platné číslo.")

    while True:
        novy_stav = input("Zadejte nový stav úkolu ('Probíhá' / 'Hotovo'): ").strip()
        if novy_stav not in ['Probíhá', 'Hotovo']:
            print("❌ Neplatný stav. Zadejte 'Probíhá' nebo 'Hotovo'.")
        else:
            break

    if update_task_status(conn, vyber_id, novy_stav):
        print("✅ Úkol byl úspěšně aktualizován.")

def get_task_id(conn,vyber_id):#pouzitie na aktualizaciu aj delete #k testu
    """
    Získa ID úlohy podľa zadaného ID.
    """
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
 
  
def kontrola_id_status(conn, vyber_id) -> bool:
    """
    Overí, či úloha so zadaným ID existuje.
    """
    id_exist = get_task_id(conn, vyber_id)
    if id_exist is None:
        return False
    return True
    
def update_task_status(conn, vyber_id, novy_stav) -> bool:
    povolene_stavy = ['Probíhá', 'Hotovo']
    if novy_stav not in povolene_stavy:
        raise ValueError("Neplatný stav úkolu")
    
    if not kontrola_id_status(conn, vyber_id):
        raise ValueError("Zadané ID neexistuje.")
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Ukoly_test SET stav = %s WHERE id = %s;", 
            (novy_stav, vyber_id)
        )
        conn.commit()
        return True
    except pymysql.MySQLError as err:
        print(f"❌ Chyba při aktualizaci úkolu: {err}")
        return False
    finally:
        cursor.close()    

#---------------------FUNKCIA ZMAZANIE ULOHY -------------------
def odstraneni_ukolu_input(conn):
    tasks = get_all_tasks(conn)
    if not tasks:
        print("Není co mazať.\n")
        return

    while True:
        try:
            vyber_id = int(input("\nZadejte ID úkolu, který chcete smazat: ")) #vstup INT, tak hlaska na Value error.
            if get_task_id(conn, vyber_id):
                potvrdenie = input(f"Opravdu chcete smazat úkol s ID {vyber_id}? Pro potvrzení akce napište 'ano'): ").strip().lower()
                if potvrdenie == 'ano':
                    if delete_task_by_id(conn, vyber_id):
                        print("✅ Úkol byl odstraněn.")
                        return
                else:
                    print("Zrušeno uživatelem.")
                    break
            else:
                print("❗ ID úkolu neexistuje.")
        except ValueError:
            print("❗ Prosím, zadejte platné číslo.")

def delete_task_by_id(conn, task_id) -> bool:
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Ukoly_test WHERE id=%s;", (task_id,))
        conn.commit()
        return cursor.rowcount > 0  # True ak sa niečo zmazalo
    finally:
        cursor.close()

#--------SPUSTENIE
conn = vytvor_pripojeni()
if conn:
    if create_table_if_not_exist(conn):
            print("✅ Tabulka je připravená.\n")
            add_task_input(conn)
            get_all_tasks(conn)
            zmen_stav_ukolu_input(conn)
            odstraneni_ukolu_input(conn)
    else:
        print("❌ Chyba při přípravě tabulky.")
        
    conn.close()
else:
    print("❌ Připojení selhalo.")
