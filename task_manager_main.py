def add_task_into_sql(conn,nazev_ukolu, popis_ukolu):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Ukoly_test (nazev, popis) VALUES (%s,%s);", 
        (nazev_ukolu.strip, popis_ukolu.strip)
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

        vysledok = add_task_overenie_input(conn, nazev_ukolu, popis_ukolu)

        if vysledok:
            print(f"\n✅ Úkol přidán: {vysledok}")
            add_task_into_sql()
            break
        else:
            print("\n❌ Název a popis musí být vyplněny.\nZkuste to znovu.\n")

# vzorove testy
# def test_pridat_ukol_vstupy_ok():
#     result = pridat_ukol_vstupy(None, "Uklidit pokoj", "Vysát a utřít prach")
#     assert result == "Uklidit pokoj: Vysát a utřít prach"

# def test_pridat_ukol_vstupy_prazdne():
#     result = pridat_ukol_vstupy(None, "   ", "  ")
#     assert result == ""