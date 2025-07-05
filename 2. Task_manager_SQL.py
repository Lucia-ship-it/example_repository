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
        print("Připojení k databázi bylo úspěšné.")
        return conn
    except pymysql.MySQLError as err:
        print(f"Chyba při připojování: {err}")


def vytvoreni_tabulky(conn): # ak este neexistuje
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Ukoly (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nazev VARCHAR (50) NOT NULL,
            popis VARCHAR (255) NOT NULL,
            stav  ENUM ('nezahájeno', 'hotovo', 'probíhá') NOT NULL DEFAULT 'nezahájeno', 
            datum_vytvoreni DATE
            )
        ''')
        print("Tabulka 'Ukoly' byla vytvořena.")
        conn.commit()
    except pymysql.MySQLError as err:
        print(f"Chyba při vytváření tabulky: {err}")
    finally:
        cursor.close()

conn = pripojeni_db()
if conn:
    vytvoreni_tabulky(conn)
    conn.close()

# v dalsej funkcii osetrit vstupy na stav ENUM 'nezahájeno', 'hotovo', 'probíhá'
#  pozor na chybz
# if input != 'nezahájeno' or input != 'hotovo' or input != 'probíhá':
# Táto podmienka bude vždy pravdivá, pretože vstup sa nikdy nemôže rovnať všetkým trom naraz. Treba to prepísať.
# urobit premennu a moznosti ako list.


