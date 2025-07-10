import pymysql
from datetime import date

def pripojeni_db():
    try:
        conn = pymysql.connect(
                host="mysql80.r4.websupport.sk",
                port=3314,
                user="EsPMMROq",
                password="79_|rBg[1F=`}cj|I%kc",
                database="Task_manager_SQL"            
            )
        print("\nPřipojení k databázi bylo úspěšné.")
        return conn
    except pymysql.MySQLError as err:
        print(f"Chyba při připojování: {err}")


def overit_existenci_tabulky_selectem(conn):
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT 1 FROM Ukoly;") #Z tabulky se nevypisují žádná skutečná data, jen testuješ, že dotaz jde provést.
        print(f"✅ Tabulka 'Ukoly' existuje.")
        return True
    except pymysql.MySQLError as err:
        if "doesn't exist" in str(err):
            print(f"ℹ️ Tabulka 'Ukoly' neexistuje.")
            return False
        else:
            print(f"❌ Jiná chyba při ověřování tabulky: {err}")
            return False
    finally:
        cursor.close()

# Vytvoření tabulky Ukoly
def vytvoreni_tabulky(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Ukoly (
                id INT PRIMARY KEY AUTO_INCREMENT,
                nazev VARCHAR(50) NOT NULL,
                popis VARCHAR(255) NOT NULL,
                stav ENUM('Nezahájeno', 'Probíhá', 'Hotovo') NOT NULL DEFAULT 'Nezahájeno',
                datum_vytvoreni DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        conn.commit()
        print("🆕 Tabulka 'Ukoly' byla vytvořena.")
    except pymysql.MySQLError as err:
        print(f"❌ Chyba při vytváření tabulky: {err}")
    finally:
        cursor.close()

# Hlavní spuštění

conn = pripojeni_db()
if not overit_existenci_tabulky_selectem(conn):
    vytvoreni_tabulky(conn)
else:
    print("✅ Tabulka je připravena.")

# moje_tuple = (1, "ahoj", 3.14)