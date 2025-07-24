import pymysql
from datetime import date
from Projekt_2.db_config import DB_CONFIG, create_connection, create_table_if_not_exist

# spustenie: python -m Projekt_2.Task_manager_TEST_SQL
def connect_to_db():
    try:
        conn = create_connection()
        print("\n✅ Připojení k databázi bylo úspěšné. Databáze Task_manager_SQL je k dispozici.")
        return conn
    
    except pymysql.MySQLError as e:
        raise ConnectionError(f"❌ Chyba při připojování: {e}")
    
    
    
#-----------------2. OVERENIE/VYTVORENIE TABULKY---------------   
def overenie_tabulky(conn):
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
       print(f"❌ Chyba při vytváření tabulky: {e}")
       raise 



#-------------------4. FUNKCIA: PRIDAJ UKOL---------------
def add_task_into_sql(conn,nazev_ukolu, popis_ukolu):
    if not nazev_ukolu.strip() or not popis_ukolu.strip():
        raise ValueError("Název a popis úkolu jsou povinné.")
    
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Ukoly_test (nazev, popis) VALUES (%s,%s);", 
        (nazev_ukolu.strip(), popis_ukolu.strip())
        )
    conn.commit()
    cursor.close()

def add_task_overenie_input(nazev_ukolu: str, popis_ukolu: str):
    nazev_ukolu = nazev_ukolu.strip()
    popis_ukolu = popis_ukolu.strip()
    if not nazev_ukolu or not popis_ukolu:
        return None
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

#-------------------5. FUNKCIA ZOBRAZIT UKOLy-----------------
    
     
        

def get_all_tasks(conn, filtruj=False)->bool:
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
            return None
        

        if filtruj == True:
            print("\n🎯 Chcete zobrazit pouze nedokončené úkoly?")
            moznost_filtru = input("\nZadejte 'filtr' pro zobrazení nedokončených úkolů, nebo stiskněte Enter pro návrat: \n").strip()
            if moznost_filtru.lower() == 'filtr':
                data_filter(conn)
        
            else:
                print("↩️  Návrat bez filtrování.")
            
        return tasks

    except pymysql.MySQLError as e:
        print(f"❌ Chyba při načítání úkolů: {e}")
    finally:
        cursor.close()

def data_filter(conn):
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT id, nazev, popis, stav FROM Ukoly_test WHERE stav IN ('Nezahájeno', 'Probíhá');"
        )
        data = cursor.fetchall()

        if data:
            print("\n📋 Seznam nedokončených úkolů:")
            for da in data:
                print(da)
        else:
            print("📭 Nemáte nedokončené úkoly.")
        return data
    finally:
        cursor.close()



#-------------------6. FUNCIA AKTUALIZACIA UKOLU----------------
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
        

def get_task_id(conn,vyber_id):
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
        return vyber_id["id"] if vyber_id else None 
    except pymysql.MySQLError as e:
        print(f"❌ Chyba při výběru id úkolu {e}")
    finally:
        cursor.close()
 
  
def kontrola_id_status(conn, vyber_id):
    """
    Overí, či úloha so zadaným ID existuje.
    """
    id_exist = get_task_id(conn, vyber_id)
    if id_exist is None:
        return None
    return id_exist
    
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
        return cursor.rowcount > 0
    finally:
        cursor.close()

#---------------------7. FUNKCIA ZMAZANIE ULOHY -------------------
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
        return cursor.rowcount > 0  # vracia počet riadkov, ktoré boli ovplyvnené posledným SQL príkazom. True ak sa niečo zmazalo
    except pymysql.MySQLError as e:
        print(f"❌ Chyba při mazání úkolu: {e}")
        return False
    finally:
        cursor.close()

#=======FUNKCIA HLAVNEHO MENU========
def hlavni_menu(conn):
   
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
            add_task_input(conn)
        elif vyber_cisla == "2":
            print("\n")
            get_all_tasks(conn, filtruj=True)
        elif vyber_cisla == "3":
            print("\nVolba Aktualizovat stav úkolu:")
            zmen_stav_ukolu_input(conn)
        elif vyber_cisla == "4":
            print("\nVolba Odstranění úkolu:")
            odstraneni_ukolu_input(conn)
        elif vyber_cisla == "5":
            print("\nKonec programu, naschledanou.👋\n")
            exit()
        else:
            print("\nZadejte správnou volbu menu.")

    
# --------SPUSTENIE
if __name__ == "__main__":
    try:
        conn = connect_to_db()
        overenie_tabulky(conn)
        hlavni_menu(conn)
    finally:  
        conn.close()