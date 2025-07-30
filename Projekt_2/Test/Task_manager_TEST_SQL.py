import pymysql
from datetime import date
from Projekt_2.db_config import DB_CONFIG, create_connection

# spustenie: python -m Projekt_2.Test.Task_manager_TEST_SQL

def connect_to_db():
    try:
        conn = create_connection()
        print("\n✅ Připojení k databázi bylo úspěšné. Databáze Task_manager_SQL je k dispozici.")
        return conn
    
    except pymysql.MySQLError as e:
        raise ConnectionError(f"❌ Chyba při připojování: {e}")
    
#-----------------2. OVERENIE/VYTVORENIE TABULKY---------------   

def table_check(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES LIKE 'Ukoly_test';")
        existuje = cursor.fetchone()

        if existuje:
            print("✅ Tabulka 'Ukoly_test' již existuje a je připravená.")
        else:    
            create_table_if_not_exist(conn)
            print("✅ Tabulka 'Ukoly_test' byla vytvořena.")
        
    except pymysql.MySQLError as e:
        raise RuntimeError(f"❌ Chyba při vytváření tabulky: {e}")
    
def create_table_if_not_exist(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Ukoly_test (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nazev VARCHAR(50) NOT NULL,
            popis VARCHAR(255) NOT NULL,
            stav ENUM('Nezahájeno', 'Probíhá', 'Hotovo') NOT NULL DEFAULT 'Nezahájeno',
            datum_vytvoreni DATE DEFAULT (CURRENT_DATE)
        );
    """)
    conn.commit()
    cursor.close()

#-------------------4. FUNKCIA: PRIDAJ UKOL---------------

def add_task_into_db(conn, nazev_ukolu, popis_ukolu):
    if not nazev_ukolu.strip() or not popis_ukolu.strip():
        raise ValueError("Název a popis úkolu jsou povinné.")
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Ukoly_test (nazev, popis) VALUES (%s,%s);",
            (nazev_ukolu.strip(), popis_ukolu.strip())
        )
        conn.commit()
        return True
    except pymysql.MySQLError as e:
        raise RuntimeError(f"Chyba při přidání úkolu: {e}")
    
    finally:
        cursor.close()
        

#----UI Pridaj ukol 

def add_task_input(conn):
    while True:
        nazev_ukolu = input("Zadejte název úkolu: ").strip()
        popis_ukolu = input("Zadejte popis úkolu: ").strip()

        if not nazev_ukolu or not popis_ukolu:
            print("\n❌ Název a popis musí být vyplněny.\nZkuste to znovu.\n")

        else:
            try:
                if add_task_into_db(conn, nazev_ukolu, popis_ukolu):
                    print(f"\n✅ Úkol: {nazev_ukolu} byl přidán.")
                    break  
            except Exception as e:
                print(f"❌ Chyba při přidávání úkolu: {e}")
              

#-------------------5. FUNKCIA ZOBRAZIT UKOLy-----------------

def get_all_tasks_from_db(conn):
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, nazev, popis, stav FROM Ukoly_test;")
        tasks = cursor.fetchall()
        return tasks
    except pymysql.MySQLError as e:
        raise ConnectionError(f"Chyba při načítání úkolů: {e}")
    finally:
        cursor.close() 
        

def get_nedokoncene_from_db(conn):
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT id, nazev, popis, stav FROM Ukoly_test WHERE stav IN ('Nezahájeno', 'Probíhá');"
        )
        tasks = cursor.fetchall()
        return tasks
    except pymysql.MySQLError as e:
        raise RuntimeError(f"❌ Chyba při načítání nedokončených úkolů: {e}")
    finally:
        cursor.close()
    

#---UI zobraz ukoly

def show_all_tasks_ui(conn, tasks_all):
    try: 
        if not tasks_all:
            print("📭 Seznam úkolů je prázdný.")
            return
        
        print("\n📋 Seznam všech úkolů:")
        for task in tasks_all:
            print(task)

        if True:
            print("\n🎯 Chcete zobrazit pouze nedokončené úkoly?")
            moznost_filtru = input("\t➤ Zadejte 'filtr' pro zobrazení nedokončených úkolů, nebo stiskněte Enter pro návrat: \n").strip()
            if moznost_filtru.lower() == 'filtr':
                data_nedokoncene = get_nedokoncene_from_db(conn)
                if data_nedokoncene:
                    print("\n📌 Seznam nedokončených úkolů:")
                    for data in data_nedokoncene:
                        print(data)
            else:
                print("↩️  Návrat bez filtrování.")

    except Exception as e:
        print(f"❌ Došlo k chybě: {e}")



#-------------------6. FUNCIA AKTUALIZACIA UKOLU----------------
    
def check_task_id(conn,vyber_id)->bool:
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT id FROM Ukoly_test WHERE id=%s;",
            (vyber_id,)
        )
        return cursor.fetchone() is not None
    except pymysql.MySQLError as e:
        raise RuntimeError(f"❌ Chyba při ověřování ID {e}")
    finally:
        cursor.close()


def update_task_status_db(conn, vyber_id, novy_stav):
    povolene_stavy = ['Probíhá', 'Hotovo']

    if novy_stav not in povolene_stavy:
        raise ValueError("Neplatný stav.")
    
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "UPDATE Ukoly_test SET stav = %s WHERE id = %s;",
            (novy_stav, vyber_id)
        )
        conn.commit()

        if cursor.rowcount == 0:
            return None  # nič sa nezmenilo
        
        # inak vrat update ulohu
        cursor.execute(
            "SELECT id, nazev, popis, stav FROM Ukoly_test WHERE id = %s;",
            (vyber_id,)
        )
        updated_task = cursor.fetchone()
        return updated_task
     
    except pymysql.MySQLError as e:
        raise ConnectionError(f"Chyba při aktualizaci úkolu: {e}")
    finally:
        cursor.close()
        

#----UI Update

def update_task_status_input(conn, tasks_all):
    try:

        if not tasks_all:
            print("Není co aktualizovat.\n")
            return
        
        print("\n📋 Seznam všech úkolů:")
        for task in tasks_all:
            print(task)
        

        while True:
            try:
                vyber_id = int(input("\nZadejte ID úkolu, jehož stav chcete změnit: "))
                if not check_task_id(conn, vyber_id):
                    print("❌ Zadané ID neexistuje. Zkuste znovu.")
                    continue
                break
            except ValueError:
                print("❌ Zadejte platné číslo.")
                continue

        while True:
            novy_stav = input("Zadejte nový stav úkolu 'Probíhá' nebo 'Hotovo': ").strip()
            try:
                if update_task_status_db(conn, vyber_id, novy_stav):
                    print("✅ Úkol byl úspěšně aktualizován.")
                    break
                else:
                    print("❌ Aktualizace se nezdařila. Zkuste to znovu")
            except ValueError as e:
                print(f"❌ {e}")  # napr. neplatný stav alebo neexistujúce ID
    except pymysql.MySQLError as e:
        print(f"❌{e}")
        
#---------------------7. FUNKCIA ZMAZANIE ULOHY -------------------
  
def delete_task_by_id(conn, task_id):
  
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Ukoly_test WHERE id=%s;", (task_id,))
        conn.commit()
        return cursor.rowcount > 0 
    except pymysql.MySQLError as e:
        raise RuntimeError(f"❌ Chyba při mazání úkolu: {e}")
    finally:
        cursor.close()

#-----UI delete

def delete_task_input(conn, tasks_all):
    try:
        if not tasks_all:
            print("Není co mazať.\n")
            return
      
        print("\n📋 Seznam všech úkolů:")
        for task in tasks_all:
            print(task)
    
        
        while True:
            try:
                vyber_id = int(input("\nZadejte ID úkolu, který chcete smazat: ")) #vstup INT, tak hlaska na Value error.
                if not check_task_id(conn, vyber_id):
                    print("❌ Zadané ID neexistuje.")
                    continue
          
                potvrdenie = input(f"Opravdu chcete smazat úkol s ID {vyber_id}?❗Pro potvrzení akce napište 'ano'): ").strip().lower()
                if potvrdenie != 'ano':
                    print("↩️  Zrušeno uživatelem.")
                    return

                if delete_task_by_id(conn, vyber_id):
                    print("✅ Úkol byl odstraněn.")
                else:
                    print("❌ Mazání se nezdařilo.")
                break
            except ValueError:
                print("❗ Prosím, zadejte platné číslo.")
    except ValueError as e:
        print(f"❌ {e}")


#=======FUNKCIA HLAVNEHO MENU========
def hlavni_menu(conn):
    tasks_all = get_all_tasks_from_db(conn)

    while True:
        print("\nSprávce úkolů - Hlavní menu")
        print("1. Přidat úkol")
        print("2. Zobrazit všechny úkoly")
        print("3. Aktualizovat stav úkolu")
        print("4. Odstranit úkol")
        print("5. Ukončit program")

        vyber_cisla=(input("Vyberte možnost (1-5):"))
                 
        if vyber_cisla == "1":
            print("\n 🔹 Přidání nového úkolu")
            add_task_input(conn)
            tasks_all = get_all_tasks_from_db(conn)
        elif vyber_cisla == "2":
            print("\n")
            show_all_tasks_ui(conn, tasks_all)
        elif vyber_cisla == "3":
            print("\nVolba Aktualizovat stav úkolu:")
            update_task_status_input(conn, tasks_all)
            tasks_all = get_all_tasks_from_db(conn)
        elif vyber_cisla == "4":
            print("\nVolba Odstranění úkolu:")
            delete_task_input(conn, tasks_all)
            tasks_all = get_all_tasks_from_db(conn)
        elif vyber_cisla == "5":
            print("\nKonec programu, naschledanou.👋\n")
            break
        else:
            print("\nZadejte správnou volbu menu.")

    
# --------SPUSTENIE
def run():
    try:
        conn = connect_to_db()
    except ConnectionError as e:
        print(f"Nelze navázat spojení s databází: {e}")
        return
    
    table_check(conn)
    hlavni_menu(conn)

    conn.close()

if __name__ == "__main__":
    run()