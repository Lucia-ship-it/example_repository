import pymysql
from datetime import date
from Projekt_2.Main.sql_funkcie import *


#-----------------UZIVATELSKE FUNKCIE-----------------
# 4. PRIDAJ UKOL
def add_task_input(conn):
    while True:
        nazev_ukolu = input("Zadejte název úkolu: ").strip()
        popis_ukolu = input("Zadejte popis úkolu: ").strip()

        if not nazev_ukolu or not popis_ukolu:
            print("\n❌ Název a popis musí být vyplněny.\nZkuste to znovu.\n")

        else:
            try:
                if add_task_into_db(conn, nazev_ukolu, popis_ukolu):
                    print(f"\n✅ Úkol: {nazev_ukolu} byl přidán.")
                    break  
            except Exception as e:
                print(f"❌ Chyba při přidávání úkolu: {e}")
              


# 5. ZOBRAZIT UKOLY
def show_all_tasks_ui(conn, tasks_all):
    try: 
        if not tasks_all:
            print("📭 Seznam úkolů je prázdný.")
            return
        
        print("\n📋 Seznam všech úkolů:")
        for task in tasks_all:
            print(task)

        if True:
            print("\n🎯 Chcete zobrazit pouze nedokončené úkoly?")
            moznost_filtru = input("\t➤ Zadejte 'filtr' pro zobrazení nedokončených úkolů, nebo stiskněte Enter pro návrat: \n").strip()
            if moznost_filtru.lower() == 'filtr':
                data_nedokoncene = get_nedokoncene_from_db(conn)
                if data_nedokoncene:
                    print("\n📌 Seznam nedokončených úkolů:")
                    for data in data_nedokoncene:
                        print(data)
            else:
                print("↩️  Návrat bez filtrování.")

    except Exception as e:
        print(f"❌ Došlo k chybě: {e}")


# 6. AKTUALIZACIA UKOLU
def update_task_status_input(conn, tasks_all):
    try:

        if not tasks_all:
            print("Není co aktualizovat.\n")
            return
        
        print("\n📋 Seznam všech úkolů:")
        for task in tasks_all:
            print(task)
        

        while True:
            try:
                vyber_id = int(input("\nZadejte ID úkolu, jehož stav chcete změnit: "))
                if not check_task_id(conn, vyber_id):
                    print("❌ Zadané ID neexistuje. Zkuste znovu.")
                    continue
                break
            except ValueError:
                print("❌ Zadejte platné číslo.")
                continue

        while True:
            novy_stav = input("Zadejte nový stav úkolu 'Probíhá' nebo 'Hotovo': ").strip()
            try:
                if update_task_status_db(conn, vyber_id, novy_stav):
                    print("✅ Úkol byl úspěšně aktualizován.")
                    break
                else:
                    print("❌ Aktualizace se nezdařila. Zkuste to znovu")
            except ValueError as e:
                print(f"❌ {e}")  # napr. neplatný stav alebo neexistujúce ID
    except pymysql.MySQLError as e:
        print(f"❌{e}")
        


# 7. ZMAZANIE ULOHY 
def odstraneni_ukolu_input(conn, tasks_all):
    try:
        if not tasks_all:
            print("Není co mazať.\n")
            return
      
        print("\n📋 Seznam všech úkolů:")
        for task in tasks_all:
            print(task)
    
        
        while True:
            try:
                vyber_id = int(input("\nZadejte ID úkolu, který chcete smazat: ")) #vstup INT, tak hlaska na Value error.
                if not check_task_id(conn, vyber_id):
                    print("❌ Zadané ID neexistuje.")
                    continue
          
                potvrdenie = input(f"Opravdu chcete smazat úkol s ID {vyber_id}?❗Pro potvrzení akce napište 'ano'): ").strip().lower()
                if potvrdenie != 'ano':
                    print("↩️  Zrušeno uživatelem.")
                    return

                if delete_task_by_id(conn, vyber_id):
                    print("✅ Úkol byl odstraněn.")
                else:
                    print("❌ Mazání se nezdařilo.")
                break
            except ValueError:
                print("❗ Prosím, zadejte platné číslo.")
    except ValueError as e:
        print(f"❌ {e}")


# 3. HLAVNE MENU
def hlavni_menu(conn):
    tasks_all = get_all_tasks_from_db(conn)

    while True:
        print("\nSprávce úkolů - Hlavní menu")
        print("1. Přidat úkol")
        print("2. Zobrazit všechny úkoly")
        print("3. Aktualizovat stav úkolu")
        print("4. Odstranit úkol")
        print("5. Ukončit program")

        vyber_cisla=(input("Vyberte možnost (1-5):"))
                 
        if vyber_cisla == "1":
            print("\n 🔹 Přidání nového úkolu")
            add_task_input(conn)
            tasks_all = get_all_tasks_from_db(conn)
        elif vyber_cisla == "2":
            print("\n")
            show_all_tasks_ui(conn, tasks_all)
        elif vyber_cisla == "3":
            print("\nVolba Aktualizovat stav úkolu:")
            update_task_status_input(conn, tasks_all)
            tasks_all = get_all_tasks_from_db(conn)
        elif vyber_cisla == "4":
            print("\nVolba Odstranění úkolu:")
            odstraneni_ukolu_input(conn, tasks_all)
            tasks_all = get_all_tasks_from_db(conn)
        elif vyber_cisla == "5":
            print("\nKonec programu, naschledanou.👋\n")
            break
        else:
            print("\nZadejte správnou volbu menu.")

    
# --------SPUSTENIE
def run():
    try:
        conn = connect_to_db()
    except ConnectionError as e:
        print(f"Nelze navázat spojení s databází: {e}")
        return
    
    table_check(conn)
    hlavni_menu(conn)

    conn.close()

if __name__ == "__main__":
    run()