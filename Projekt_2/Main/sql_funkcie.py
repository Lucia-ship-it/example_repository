import pymysql
from datetime import date
from Projekt_2.db_config import DB_CONFIG, create_connection


#-----------------DATABAZOVE FUNKCIE -----------------
# 1. PRIPOJENIE DO DB
def connect_to_db():
    try:
        conn = create_connection()
        print("\n✅ Připojení k databázi bylo úspěšné. Databáze Task_manager_SQL je k dispozici.")
        return conn
    
    except pymysql.MySQLError as e:
        raise ConnectionError(f"❌ Chyba při připojování: {e}")
    
# 2. OVERENIE/VYTVORENIE TABULKY
def table_check(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES LIKE 'Ukoly';")
        existuje = cursor.fetchone()

        if existuje:
            print("✅ Tabulka 'Ukoly' již existuje a je připravená.")
        else:    
            create_table_if_not_exist(conn)
            print("✅ Tabulka 'Ukoly' byla vytvořena.")
        
    except pymysql.MySQLError as e:
        raise RuntimeError(f"❌ Chyba při vytváření tabulky: {e}")
    
def create_table_if_not_exist(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Ukoly (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nazev VARCHAR(50) NOT NULL,
            popis VARCHAR(255) NOT NULL,
            stav ENUM('Nezahájeno', 'Probíhá', 'Hotovo') NOT NULL DEFAULT 'Nezahájeno',
            datum_vytvoreni DATE DEFAULT (CURRENT_DATE)
        );
    """)
    conn.commit()
    cursor.close()

# 4. PRIDAJ UKOL
def add_task_into_db(conn, nazev_ukolu, popis_ukolu):
    if not nazev_ukolu.strip() or not popis_ukolu.strip():
        raise ValueError("Název a popis úkolu jsou povinné.")
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Ukoly (nazev, popis) VALUES (%s,%s);",
            (nazev_ukolu.strip(), popis_ukolu.strip())
        )
        conn.commit()
        return True
    except pymysql.MySQLError as e:
        raise RuntimeError(f"Chyba při přidání úkolu: {e}")
    
    finally:
        cursor.close()

# 5. ZOBRAZIT UKOLY
def get_all_tasks_from_db(conn):
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, nazev, popis, stav FROM Ukoly;")
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
            "SELECT id, nazev, popis, stav FROM Ukoly WHERE stav IN ('Nezahájeno', 'Probíhá');"
        )
        tasks = cursor.fetchall()
        return tasks
    except pymysql.MySQLError as e:
        raise RuntimeError(f"❌ Chyba při načítání nedokončených úkolů: {e}")
    finally:
        cursor.close()
    
# 6. AKTUALIZACIA UKOLU
def check_task_id(conn,vyber_id)->bool:
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT id FROM Ukoly WHERE id=%s;",
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
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Ukoly SET stav = %s WHERE id = %s;",
            (novy_stav, vyber_id)
        )
        conn.commit()
        return cursor.rowcount > 0
    except pymysql.MySQLError as e:
        raise ConnectionError(f"Chyba při aktualizaci úkolu: {e}")
    finally:
        cursor.close()

# 7. ZMAZANIE ULOHY 
def delete_task_by_id(conn, task_id):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Ukoly WHERE id=%s;", (task_id,))
        conn.commit()
        return cursor.rowcount > 0 
    except pymysql.MySQLError as e:
        raise RuntimeError(f"❌ Chyba při mazání úkolu: {e}")
    finally:
        cursor.close()