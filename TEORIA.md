----------------✅ Modulárne programovanie + testovateľnosť-------------
instalacia venv a pip
instalacia pytest pip3 install -U pytest

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


Testy budou pracovat s hlavní databází nebo s testovací databází. Testovací data se budou dynamicky přidávat.Každá funkce musí mít 2 testy: 
1. Pozitivní test – Ověří správnou funkčnost operace.
2. Negativní test – Ověří, jak program reaguje na neplatné vstupy.

V zadání „Testovací data se budou dynamicky přidávat“ znamená, že během běhu testů (tedy dynamicky, ne předem) budou do databáze vkládána testovací data přímo testovacím kódem.
Co to znamená v praxi?
Testy nepoužívají jen statická data, která jsou už předem v databázi.

Místo toho testy při spuštění sami vloží potřebná data do databáze (například vložením záznamů přes SQL příkazy nebo pomocí ORM).

Po dokončení testu se často data zase vymažou (či databáze resetuje), aby testy byly izolované a neměly vliv na další testy.

!!! funkčnost operací: přidání, aktualizace a odstranění úkolů pomocí pytest
nakonci zmazat testovacie data

cd /Users/luciakobzova/example_repository/Projekt_2

///////////////////////////////////////////////

.env = slúži na ukladanie citlivých alebo konfiguračných údajov mimo zdrojového kódu – napríklad:

prihlasovacie údaje (heslá, API kľúče),

databázové pripojenia,

špecifické nastavenia pre beh aplikácie.

Používa sa hlavne preto, aby tieto údaje:

neboli napevno napísané v kóde, a

neboli náhodne nahrané na GitHub.

---------------

main.py - hlavny subor, bezna prax
v main je zalozeny dynamicky import
# instalacia : pip3 install python-dotenv

TO CO TESTUJEME JE PRAVDEPODOBNE ZLE< NEMOZEME TOMU VERIT> MUSIME SI  v teste vlastne pripojenie

///// uprava projektu
Nekonzistentní návratové hodnoty: Někde se vrací prázdný řetězec, jinde None, jinde False.

✅ Čo upraviť:
Vyber si jedno pravidlo:

Pre "nič sa nenašlo" používaj vždy None

Pre "neúspešnú operáciu" používaj False

V komentároch k funkciám jasne napíš, čo funkcia vracia v každom prípade.

aby sme nekopirovali kod / lebo moze vrniknut chyba / vytvorime si pytest parametrise - prepiseme funkciu, ktora sa opakuje

pridat_ulohu(nazov, popis, stav)
aj v selecte aby bolo %s

to iste v assert - miesto realnych hodnot name, popis, stav
pouzitie s dekoratorom nad funkciou
@pytest.mark.parametrize(
"nazev, popis, stav",
[(ukol 1, popis1, Hotovo),
(uko2, popis 2, Probiha)]
)

VYTKA
Někde se vrací prázdný řetězec, jinde None, jinde False. Doporučujeme sjednotit vracenou hodnotu pro chybějící vstup.

Toto je oprávnená výtka a týka sa najmä funkcií, ktoré pracujú s chybovými alebo "ničím" výsledkami. Nekonzistentnosť môže viesť k nejasnému spracovaniu alebo chybám pri použití funkcií.