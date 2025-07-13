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
        # return tasks
        if tasks:
            print("\n📋 Seznam všech úkolů:")
            for task in tasks:
                print(task)
        else:
            print("📭 Seznam úkolů je prázdný.")

    except pymysql.MySQLError as err:
        print(f"❌ Chyba při načítání úkolů: {err}")
        return []
    finally:
        cursor.close()

    
#-----------AKTUALIZACIA--------
def zmen_stav_ukolu_input(conn):
    get_all_tasks(conn)

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

    # if id_exist is None:
    #     raise ValueError("Zadané ID neexistuje.")
    
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

#--------SPUSTENIE
conn = vytvor_pripojeni()
if conn:
    if create_table_if_not_exist(conn):
            print("✅ Tabulka je připravená.\n")
            zmen_stav_ukolu_input(conn)
    else:
        print("❌ Chyba při přípravě tabulky.")
        
    conn.close()
else:
    print("❌ Připojení selhalo.")



#mozne testy
# def test_kontrola_id_status_existujici(conn):
#     assert kontrola_id_status(conn, 1) == True

# def test_kontrola_id_status_neexistujici(conn):
#     assert kontrola_id_status(conn, 9999) == False

# def test_update_task_status_valid(conn):
#     assert update_task_status(conn, 1, "Hotovo") == True

# def test_update_task_status_neplatny_stav(conn):
#     try:
#         update_task_status(conn, 1, "Neznámy stav")
#     except ValueError as e:
#         assert str(e) == "Neplatný stav úkolu."

# def test_update_task_status_neexistujuce_id(conn):
#     try:
#         update_task_status(conn, 9999, "Hotovo")
#     except ValueError as e:
#         assert str(e) == "Zadané ID neexistuje."