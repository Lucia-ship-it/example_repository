from ukoly_logika import add_task_overenie_input
from ukoly_sql import add_task_into_sql

#funkcie s input()/print()

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