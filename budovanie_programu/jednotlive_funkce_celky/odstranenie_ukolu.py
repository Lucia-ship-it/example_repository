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

def get_all_tasks(conn):
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, nazev, popis, stav FROM Ukoly_test;")
        tasks = cursor.fetchall()  # ✅ dá sa testovať pomocou assert
        
        if tasks:
            print("\nSeznam všech úkolů:")
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

# ------ROZDIEL PRINT A RETURN-----
# „Mám 0 jabĺk.“ (to je výpis – print)
# Ale ty sa ho musíš opýtať:
# „Koľko jabĺk máš?“ (to je return), aby si mohla rozhodnúť, čo ďalej.

#----------ODSTANENIE ULOHY-----------------

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
            odstraneni_ukolu_input(conn)

    else:
        print("❌ Chyba při přípravě tabulky.")
        
    conn.close()
else:
    print("❌ Připojení selhalo.")


#mozne testy
# def test_delete_task_success(conn):
#     # Najskôr si vložíme testovací úkol
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO Ukoly_test (nazev, popis) VALUES ('Test úkol', 'Na smazání');")
#     conn.commit()
#     task_id = cursor.lastrowid
#     cursor.close()

#     assert get_task_id(conn, task_id) == task_id

#     result = delete_task_by_id(conn, task_id)
#     assert result is True

#     assert get_task_id(conn, task_id) is None