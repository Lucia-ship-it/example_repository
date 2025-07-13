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
    
#-----------------OVERENIE/VYTVORENIE TABULKY---------------   
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

#-------------------FUNKCIA: PRIDAJ UKOL---------------
def add_task_into_sql(conn,nazev_ukolu, popis_ukolu):
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
        return ""
    return f"{nazev_ukolu}: {popis_ukolu}" 
   
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

#-------------------FUNKCIA ZOBRAZIT UKOLy-----------------





#-------------------FUNCIA AKTUALIZACIA UKOLU----------------


#---------------------FUNKCIA ZMAZANIE ULOHY -------------------











    conn = vytvor_pripojeni()
    if conn:
        if create_table_if_not_exist(conn):
            print("✅ Tabulka je připravená.")
        else:
            print("❌ Chyba při přípravě tabulky.")
    else:
        print("❌ Nepodařilo se připojit k databázi.")
   
    conn.close()

  