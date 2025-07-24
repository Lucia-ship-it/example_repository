import pymysql
from pymysql.err import MySQLError
from datetime import date
from db_config import DB_CONFIG, create_connection, create_table_if_not_exist

def connect_to_db():
    try:
        conn = create_connection()
        print("\n✅ Připojení k databázi bylo úspěšné. Databáze Task_manager_SQL je k dispozici.")
        return conn
    
    except MySQLError as e:
        raise ConnectionError(f"❌ Chyba při připojování: {e}")
    
    
    
#-----------------2. OVERENIE/VYTVORENIE TABULKY---------------   
def overenie_tabulky():
    try:
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES LIKE 'Ukoly_test';")
        existuje = cursor.fetchone()

        if existuje:
            print("✅ Tabulka 'Ukoly_test' již existuje a je připravená.")
        else:    
            create_table_if_not_exist(conn)
            print("✅ Tabulka 'Ukoly_test' byla vytvořena.")
        

    except MySQLError as e:
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

def add_task_overenie_input(nazev_ukolu: str, popis_ukolu: str) -> str: # -> oznacuje, ze funkccia vrati retazec. 
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
    
def get_all_tasks_moznost_filtra(conn, moznost_filtru=None):
    if moznost_filtru is None:
        moznost_filtru = input("\nV případě, že si přejete zobrazit pouze nedokončené úkoly, napište 'filtr': \n").strip()
    
    if moznost_filtru == 'filtr':
        data_filter(conn)
        
    else:
        print("Zrušeno uživatelem.")
        return
        

def get_all_tasks(conn, filtruj=False):
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
            get_all_tasks_moznost_filtra(conn)
 #musi byt v tele, inak sa ani nezobrazi a msim osetrit parametrom, aby sa mi nezobrazoval filter aj pri aktualizacii
        return tasks # vzdy vrati zoznam, bud s hodnotami alebo bez

    except pymysql.MySQLError as err:
        print(f"❌ Chyba při načítání úkolů: {err}")
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
if __name__ == "__main__": # Aby sa program spustil len vtedy, keď súbor spúšťaš priamo, ale nie pri importe (napr. z testov)
    try:
        conn = connect_to_db()
        overenie_tabulky()
        hlavni_menu(conn)
    finally:  
        conn.close()

