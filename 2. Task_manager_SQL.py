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
        print("\nPřipojení k databázi bylo úspěšné.")
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
            stav  ENUM ('Nezahájeno', 'Probíhá', 'Hotovo') NOT NULL DEFAULT 'nezahájeno', 
            datum_vytvoreni DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        print("Tabulka 'Ukoly' byla vytvořena.")
        conn.commit()
    except pymysql.MySQLError as err:
        print(f"Chyba při vytváření tabulky: {err}")
    finally:
        cursor.close()


# pridanie prvých záznamov do tabulky - vzorove ukoly
def pridani_vzorovych_ukolu(conn):
    '''pridanie 2 vzorovych uloh'''
    try:
        cursor = conn.cursor()
        dnes = date.today()
        ulohy_exmpl = [
            ("úkol 1", "popis k úkolu 1", "probíhá", dnes),
            ("úkol 2", "popis k úkolu 2", "hotovo", dnes)
        ]
        cursor.executemany(
            "INSERT INTO Ukoly (nazev, popis, stav) VALUES (%s, %s, %s);",
            ulohy_exmpl
        )
        conn.commit()
        print("✅ Přidání vzorových úkolů proběhlo v pořádku")
    except pymysql.MySQLError as err:
        print(f"Chyba při přidávání úkolů: {err}")
    finally:
        cursor.close()



# 3. hlavni_menu() – Hlavní nabídka
# OK  Zobrazí možnosti:
# OK  1. Přidat úkol
# OK  2. Zobrazit úkoly
# OK  3. Aktualizovat úkol
# OK  4. Odstranit úkol
# OK  5. Ukončit program
# OK  Pokud uživatel zadá špatnou volbu, program ho upozorní a nechá ho vybrat znovu.
def hlavni_menu(conn):
   
     while True:
        print("\nSprávce úkolů - Hlavní menu")
        print("1. Přidat úkol")
        print("2. Zobrazit všechny úkoly")
        print("3. Aktualizovat úkol")
        print("4. Odstranit úkol")
        print("5. Ukončit program")
        try:
            vyber_cisla=int(input("Vyberte možnost (1-4):"))
            if vyber_cisla == 1:
                print("\nPřidání nového úkolu")
                pridat_ukol_sql(conn)
            elif vyber_cisla == 2:
                print("\nZobrazení všech úkolů:")
                zobrazit_ukoly(conn)
            elif vyber_cisla == 3:
                print("\nVolba Aktualizovat úkol:")
                aktualizace_ukolu(conn)
            elif vyber_cisla == 4:
                print("\nVolba Odstranění úkolu:")
            elif vyber_cisla == 5:
                print("\nKonec programu, naschledanou.\n")
                exit()
        except ValueError:
            print("\nZadejte správnou volbu menu.")

# 4. pridat_ukol() – Přidání úkolu
# OK Uživatel zadá název a popis úkolu.
# OK Povinné údaje: Název i popis jsou povinné, nesmí být prázdné.
# OK - Automatické hodnoty:
# OK    1. Úkol dostane ID automaticky.
# OK    2. Výchozí stav ukolu: Nezahájeno
# OK - Po splnění všech podmínek se úkol uloží do databáze

def pridat_ukol_sql(conn):
    '''Získaj vstupy od používateľa a ulož úlohu do DB'''
    while True: #osetrenie prazdneho vstupu
        nazev_ukolu = input("Zadejte název úkolu: ").strip()
        if nazev_ukolu == "":
            print("\nVyplnění je povinné\n")
        else:
            break

    while True:
       popis_ukolu = input("Zadejte popis úkolu: ").strip()
       if popis_ukolu == "":
            print("\nVyplnění je povinné\n")
       else:
            break

    try: 
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "INSERT INTO Ukoly (nazev, popis) VALUES (%s,%s);", 
            (nazev_ukolu, popis_ukolu)
            )
        conn.commit()

# zobrazenie posledneho ukolu
        cursor.execute(
            "SELECT * From Ukoly ORDER BY id DESC LIMIT 1;"
            )
        posledny_ukol = cursor.fetchone()
        print(f"Přidali jste nový úkol: {posledny_ukol}")

    
    except pymysql.MySQLError as err:
        print(f"❌ Chyba při ukládání do databáze: {err}")

    finally:
        cursor.close()


# v dalsej funkcii osetrit vstupy na stav ENUM 'nezahájeno', 'hotovo', 'probíhá'
#  pozor na chybz
# if input != 'nezahájeno' or input != 'hotovo' or input != 'probíhá':
# Táto podmienka bude vždy pravdivá, pretože vstup sa nikdy nemôže rovnať všetkým trom naraz. Treba to prepísať.
# urobit premennu a moznosti ako list.

# def osetrenie_vstupu_pre_stav():
#     stav_dovolene_vstupy = ['nezahájeno', 'hotovo', 'probíhá']
#     stav_ukolu = input("Napište, v jakém stavu je váš úkol. Možnosti: nezahájeno, hotovo, probíhá.").lower().strip()
#     if stav in stav_dovolene_vstupy:
#         try:
#             #funkcia pre zapisanie stavu do tabulky.
#         except pymysql.MySQLError:
#             print("Zadej správný výběr stavu úkolu")
#             return

# 5. zobrazit_ukoly() – Zobrazení úkolů
# OK Seznam všech úkolů s informacemi: ID, název, popis, stav.
# OK Filtr: Zobrazí pouze úkoly se stavem "Nezahájeno" nebo "Probíhá".
# - Pokud nejsou žádné úkoly, zobrazí informaci, že seznam je prázdný.
def zobrazit_ukoly(conn):
    print("\nSeznam všech úkolů:") 
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(
        "SELECT id, nazev, popis, stav FROM Ukoly;"
        )
    ukoly_vsechny = cursor.fetchall()
    if len(ukoly_vsechny) == 0:
        print("Seznam úkolů je prázdný")
    for ukol in ukoly_vsechny:
        print(ukol)
    cursor.close()

def zobrazeni_nedokoncenych_ukolu(conn):
    print("\nZobrazení nedokončených úkolů: ")
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(
        "SELECT id, nazev, popis, stav FROM Ukoly WHERE stav IN ('nezahájeno', 'probíhá');"
        )
    ukoly_vyber_stav = cursor.fetchall()
    for u in ukoly_vyber_stav:
        print(u)
    cursor.close()

# 6. aktualizovat_ukol() – Změna stavu úkolu
# OK Uživatel vidí seznam úkolů (ID, název, stav).
# OK Vybere úkol podle ID.
# OK Dostane na výběr nový stav: "Probíhá" nebo "Hotovo"
# OK Po potvrzení se aktualizuje DB.
# OK Pokud zadá neexistující ID, program ho upozorní a nechá ho vybrat znovu.

      
#vstav dat do formatu na vyber cisla, aby to nemusel s diakritikou vyplnat. podobne ako vyber 

def aktualizace_ukolu(conn):
    print("\nSeznam úkolů:")
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(
        "SELECT id, nazev, stav FROM Ukoly;"
                )
    vsechny_ukoly_vyber = cursor.fetchall()
    for ukol_vyber in vsechny_ukoly_vyber:
        print(ukol_vyber)
    vsechna_id = [ukol['id'] for ukol in vsechny_ukoly_vyber]
    
    # Vybere úkol podle ID.
    while True:
        try:
            vyber_ukolu_id = int(input("\nZadejte ID úkolu, který chcete upravit: ")) # musime osetrit ValueError, keby sa nezada cislo

            if vyber_ukolu_id in vsechna_id:
                print(f"K úpravě jste vybrali úlohu s id {vyber_ukolu_id}.")
                cursor.execute(
                    "SELECT id, nazev, popis, stav FROM Ukoly WHERE id=%s;",
                    (vyber_ukolu_id,) #SQL parametr (vyber_ukolu_id) musí být TUPLE (vyber_ukolu_id,)
                )
                ukazka_ukolu = cursor.fetchone()
                print(ukazka_ukolu)
                break
            else:
                print("\nZadejte správnou hodnotu id.")
        except ValueError:
            print("\n❗ Prosím, zadejte platné číslo.")
        except pymysql.MySQLError as err:
            print(f"❌ Chyba při výběru id úkolu {err}")
            
      
    while True:
        print("\nZadejte stav úkolu výběrem z možností: 'Probíhá', 'Hotovo'" )
        hodnoty_stavu = ['Probíhá', 'Hotovo']
        stav = input("Nový stav: ").strip()

        if  stav in hodnoty_stavu:
            cursor.execute(
                "UPDATE Ukoly SET stav = %s WHERE id = %s;", 
                ( stav, vyber_ukolu_id)
                )
            conn.commit()
            print("\n✅ Úkol byl úspěšně aktualizován.\nNyní budete přesměrováni do hlavního menu.")
            return
        else:
            print("\nZadejte správnou hodnotu pro stav")
        
    
    

# 7. odstranit_ukol() – Odstranění úkolu
# - Uživatel vidí seznam úkolů.
# -  Vybere úkol podle ID.
# - Po potvrzení bude úkol trvale odstraněn z databáze.
# - Pokud uživatel zadá neexistující ID, program ho upozorní a nechá ho vybrat znovu.

#------SPURSTENIE PROGRAMU-------

conn = pripojeni_db()
if conn:
    vytvoreni_tabulky(conn)
    print("Databáze Task_manager_SQL je k dispozici.\n")
    hlavni_menu(conn)
    conn.close()
   