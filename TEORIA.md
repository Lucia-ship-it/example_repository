----------------✅ Modulárne programovanie + testovateľnosť-------------

1. napisem si funkcie, ktore nepouzivaju input ani print - lahko otestovatelne
po logickych kusoch, kludne do zvlast suboru
2. Používateľský kód (menu, input...) daj do main.py. tu sa pouzije print
priklad:
from ukoly import kontrola_id_status, update_task_status, get_all_tasks

def aktualizace_ukolu(conn):
    get_all_tasks(conn)
    try:
        id = int(input("Zadejte ID úkolu: "))
        kontrola_id_status(conn, id)
        stav = input("Zadejte nový stav (Probíhá / Hotovo): ")
        update_task_status(conn, id, stav)
        print("✅ Úkol byl aktualizován.")
    except ValueError as e:
        print(f"❌ {e}")

3. Testovanie robíš v súbore test_ukoly.py
projekt/
│
├── ukoly.py          # funkcie pre prácu s databázou
├── main.py           # hlavný program (menu, inputy)
├── test_ukoly.py     # testy cez pytest
└── requirements.txt  # ak budeš inštalovať knižnice

projekt/
├── ukoly_sql.py          ← obsahuje databázové funkcie (SQL)
├── ukoly_logika.py       ← čistá logika bez input()/print() → testovateľná
├── ukoly_input.py        ← funkcie s input()/print()
├── test_ukoly_logika.py  ← pytest testy pre logiku
└── main.py               ← spúšťací súbor (napr. menu, výber akcií)

----> POSTUP <------ 
Napíšeš funkciu → napr. kontrola_id_status
Vyskúšaš ju cez pytest v test_ukoly.py
Ak funguje, použiješ ju v main.py pri zadávaní úlohy
