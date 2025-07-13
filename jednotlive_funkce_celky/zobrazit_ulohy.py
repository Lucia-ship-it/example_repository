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

#----------NOVA FUNKCIA ZOBRAZIT UKOLY ------        
def get_all_tasks(conn):
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, nazev, popis, stav FROM Ukoly_test;")
        tasks = cursor.fetchall()  # ✅ dá sa testovať pomocou assert
        
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

#---------------------------------------------
#v MAIN zobrazit pouzivatelovi

conn = vytvor_pripojeni()
if conn:
    if create_table_if_not_exist(conn):
            print("✅ Tabulka je připravená.\n")
            get_all_tasks(conn)
    else:
        print("❌ Chyba při přípravě tabulky.")
        
    conn.close()
else:
    print("❌ Připojení selhalo.")




# from ukoly_sql import get_all_tasks

# def test_get_all_tasks_not_empty():
#     conn = vytvor_pripojeni()
#     tasks = get_all_tasks(conn)
#     assert isinstance(tasks, list)
#     assert all("id" in task and "stav" in task for task in tasks)
#     conn.close()


# from ukoly_sql import data_filter

# def test_data_filter_returns_only_not_done_tasks():
#     conn = vytvor_pripojeni()
#     filtered = data_filter(conn)
#     assert all(task["stav"] in ["Nezahájeno", "Probíhá"] for task in filtered)
#     conn.close()

# from ukoly_sql import get_all_tasks
# from pripojeni import vytvor_pripojeni

# def test_get_all_tasks_has_some_data():
#     conn = vytvor_pripojeni()
#     tasks = get_all_tasks(conn)

#     assert isinstance(tasks, list)
#     assert len(tasks) > 0  # ✅ overí, že zoznam nie je prázdny

#     conn.close()

# def test_get_all_tasks_not_empty():
#     conn = vytvor_pripojeni()
#     tasks = get_all_tasks(conn)

#     assert len(tasks) > 0, "❌ Zoznam úloh je prázdny, očakávané aspoň 1 úloha."









#PRIDANIE, ZOBRAZENIE, ZMAZANIE
# 
# from ukoly_sql import get_all_tasks
# from pripojeni import vytvor_pripojeni

# def test_get_all_tasks_with_temp_data():
#     conn = vytvor_pripojeni()
#     cursor = conn.cursor()

#     # 🔧 SETUP – vloženie testovacej úlohy
#     cursor.execute(
#         "INSERT INTO Ukoly_test (nazev, popis, stav) VALUES (%s, %s, %s);",
#         ("Testovací úkol", "Toto je test", "Nezahájeno")
#     )
#     conn.commit()

#     # Získanie ID testovacieho záznamu
#     cursor.execute("SELECT LAST_INSERT_ID();")
#     test_id = cursor.fetchone()[0]

#     # 🧪 TEST
#     tasks = get_all_tasks(conn)
#     assert any(task["id"] == test_id for task in tasks), "Testovací úkol sa nenašiel v zozname."

#     # 🧹 TEARDOWN – zmazanie testovacieho záznamu
#     cursor.execute("DELETE FROM Ukoly_test WHERE id = %s;", (test_id,))
#     conn.commit()

#     cursor.close()
#     conn.close()


