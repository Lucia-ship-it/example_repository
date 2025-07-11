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
        print("\nPřipojení k databázi bylo úspěšné. Databáze Task_manager_SQL je k dispozici.")
        
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

#test
# vysledok = create_table_if_not_exist(conn)
# assert vysledok is True  # ⬅️ overenie cez assert

# # Overenie existencie tabuľky
# with conn.cursor() as cursor:
# cursor.execute("SHOW TABLES LIKE 'Ukoly_test';")
# assert cursor.fetchone() is not None


# Hlavní spuštění
conn = vytvor_pripojeni()
if create_table_if_not_exist(conn):
        print("✅ Tabulka je připravená.")
else:
    print("❌ Chyba při přípravě tabulky.")
conn.close()