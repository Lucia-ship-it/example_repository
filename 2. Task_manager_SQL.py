import pymysql
from datetime import date

# zadanie
# Použití MySQL databáze: Vytvoříte databázovou tabulku ukoly, která bude obsahovat: 
# - id 
# - nazev
# - popis
# - stav (nezahájeno, hotovo, probíhá)
# - datum vytvoreni

# ---------- Funkce programu ----------
# 1. pripojeni_db() – Připojení k databázi
# OK Funkce vytvoří připojení k MySQL databázi.
# OK Pokud připojení selže, zobrazí chybovou zprávu.
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

# 2. vytvoreni_tabulky() – Vytvoření tabulky, pokud neexistuje
# OK - Funkce vytvoří tabulku ukoly, pokud ještě neexistuje.
# OK - Ověří existenci tabulky v databázi.

def vytvoreni_tabulky(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Ukoly (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nazev VARCHAR (50) NOT NULL,
            popis VARCHAR (255) NOT NULL,
            stav  ENUM ('nezahájeno', 'hotovo', 'probíhá') NOT NULL, 
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
    print("Tabulka 'Ukoly' je k dispozici.")
    conn.close()

# pridanie prvých záznamov do tabulky - vzorove ukoly
def pridani_vzorovych_ukolu(conn):
    '''pridanie 2 vzorovych uloh'''
    try:
        cursor = conn.cursor()
        ulohy_exmpl = [
            ("úkol 1", "popis k úkolu 1", "probíhá"),
            ("úkol 2", "popis k úkolu 2", "hotovo")
        ]
        cursor.executemany(
            "INSERT INTO Ukoly (nazev, popis, stav) VALUES (%s, %s, %s)",
            ulohy_exmpl
        )
        cursor.commit()
        print("✅ Přidání vzorových úkolů proběhlo v pořádku")
    except pymysql.MySQLError as err:
        print(f"Chyba při přidávání knih: {err}")
    finally:
        cursor.close()



# 3. hlavni_menu() – Hlavní nabídka
#  - Zobrazí možnosti:
#     1. Přidat úkol
#     2. Zobrazit úkoly
#     3. Aktualizovat úkol
#     4. Odstranit úkol
#     5. Ukončit program
# - Pokud uživatel zadá špatnou volbu, program ho upozorní a nechá ho vybrat znovu.

# 4. pridat_ukol() – Přidání úkolu
#   - Uživatel zadá název a popis úkolu.
#  - Povinné údaje: Název i popis jsou povinné, nesmí být prázdné.
# - Automatické hodnoty:
#     1. Úkol dostane ID automaticky.
#     2. Výchozí stav ukolu: Nezahájeno
# - Po splnění všech podmínek se úkol uloží do databáze

nazev_ukolu = input(“Zadejte název úkolu”)
popis_ukolu = input(“Zadejte popis úkolu”)
cursor.execute(“INSERT INTO Ukoly (nazov, popis, stav) VALUES (%s,%s,%s), (nazev, popis, stav)

# v dalsej funkcii osetrit vstupy na stav ENUM 'nezahájeno', 'hotovo', 'probíhá'
#  pozor na chybz
# if input != 'nezahájeno' or input != 'hotovo' or input != 'probíhá':
# Táto podmienka bude vždy pravdivá, pretože vstup sa nikdy nemôže rovnať všetkým trom naraz. Treba to prepísať.
# urobit premennu a moznosti ako list.

def osetrenie_vstupu_pre_stav():
    stav_dovolene_vstupy = ['nezahájeno', 'hotovo', 'probíhá']
    stav_ukolu = input("Napište, v jakém stavu je váš úkol. Možnosti: nezahájeno, hotovo, probíhá.").lower().strip()
    if stav in stav_dovolene_vstupy:
        try:
            #funkcia pre zapisanie stavu do tabulky.
        except:
        print("Zadej správný výběr stavu úkolu")
        return
# 5. zobrazit_ukoly() – Zobrazení úkolů
# OK Seznam všech úkolů s informacemi: ID, název, popis, stav.
# OK Filtr: Zobrazí pouze úkoly se stavem "Nezahájeno" nebo "Probíhá".
# - Pokud nejsou žádné úkoly, zobrazí informaci, že seznam je prázdný.
def zobrat_ukoly():
    cursor.execute("SELECT id, nazev, popis, stav FROM UKOLY")
    ukoly_vsechny = cursor.fetchall()
    return ukoly_vsechny
    cursor.close()

def zobrazeni_nedokoncenych_ukolu():
    cursor.execute("SELECET id, nazev, popis, stav FROM UKOLY WHERE stav IN (Nezahájeno, Probíhá)")
    ukoly_vyber_stav = cursor.fetchall()
    return ukoly_vyber_stav
    cursor.close()


# 6. aktualizovat_ukol() – Změna stavu úkolu
# - Uživatel vidí seznam úkolů (ID, název, stav).
# - Vybere úkol podle ID.
# - Dostane na výběr nový stav: "Probíhá" nebo "Hotovo"
# - Po potvrzení se aktualizuje DB.
# -  Pokud zadá neexistující ID, program ho upozorní a nechá ho vybrat znovu.

# 7. odstranit_ukol() – Odstranění úkolu
# - Uživatel vidí seznam úkolů.
# -  Vybere úkol podle ID.
# - Po potvrzení bude úkol trvale odstraněn z databáze.
# - Pokud uživatel zadá neexistující ID, program ho upozorní a nechá ho vybrat znovu.