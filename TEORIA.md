# spustenie: example_repository % python -m Projekt_2.Main.Task_manager_SQL

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

✅ Používať výnimky (raise) na skutočné chyby
-Prázdny vstup
-Neexistujúce ID
-Chyby v DB
Odporúčanie:
-Výnimka je tu dobrá na validáciu vstupu, overenie pripojenie, vytvorenia tabulky
-Chybu chceš hneď vidieť, nemá zmysel ticho zlyhať.



✅ Používať návratové hodnoty (None/False) na neutrálne stavy
-Zoznam je prázdny
-Užívateľ zrušil akciu
-Nič sa nezmenilo

🧠 Rozdiel: except s raise vs. bez raise
Prístup	Význam	Kedy použiť
except ValueError as e: print(...) (bez raise)	Výnimku zachytíš a spracuješ priamo v mieste – už ju ďalej nešíriš.	Ak chceš používateľovi hneď ukázať, čo sa pokazilo, a pokračovať
except ValueError as e: raise	Výnimku zachytíš, ale ju znova vyhodíš na vyššiu úroveň.	Ak chceš, aby vyššia vrstva aplikácie vedela, že došlo k chybe a rozhodla, čo ďalej

typy RAISE
ConnectionError 	Problémy s pripojením k DB
ValueError	        Zlé/neplatné ID alebo parametre
LookupError	        Neúspešné vyhľadanie v dátach
RuntimeError        Záložná možnosť – keď nič iné nepasuje


najskor osetrim negativne spravanie a potom vystup toho co chcem vidiet
Tento prístup sa často nazýva - early exit- alebo -guard clause- a patrí medzi dobré praktiky v programovaní. Znamená to, že najskôr ošetruješ výnimočné alebo negatívne prípady, aby si mohol potom s istotou riešiť ten "normálny" alebo "správny" tok kódu.

        if not data:  # ak je prázdny zoznam alebo None
            print("📭 Nemáte nedokončené úkoly.")
            return None
        
        print("\n📋 Seznam nedokončených úkolů:")
        for da in data:
            print(da)
        return data

UI oddelene:
Máš funkcie ako add_task_into_sql, update_task_status, delete_task_by_id — tie by mali byť „čisté“ v tom, že iba vykonávajú operáciu nad DB a v prípade chyby vyhodia výnimku (alebo vrátia úspech/ neúspech). Nemali by riešiť nič s UI (napr. printovanie, input, pýtanie sa používateľa, opakovanie vstupov).

Naopak, UI funkcie (add_task_input, zmen_stav_ukolu_input, odstraneni_ukolu_input) sú zodpovedné za komunikáciu s používateľom — pýtajú sa na vstupy, vypisujú správy, opakujú vstupy, riešia potvrdenia, a na základe toho volajú „čisté“ DB funkcie.

duplicitne volania: 
Duplicitné volania get_task_id()
V niektorých funkciách (napr. update_task_status aj delete_task_by_id) sa overuje ID viackrát – najskôr v UI, potom ešte v SQL funkcii.

Odporúčanie: Over ID len v UI vrstve a nech SQL funkcie predpokladajú, že ID už existuje – tým znížiš duplikáciu a zjednodušíš logiku.

co robi continue vo funkcii:
def odstraneni_ukolu_input(conn):
    try:
        tasks = get_all_tasks_sql(conn)
        if not tasks:
            print("Není co mazať.\n")
            return
        show_tasks(tasks)
        
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

- Skontroluje, či ID existuje v databáze.
- ❌ Ak neexistuje, vypíše hlášku.
- continue zabezpečí, že sa cyklus vráti späť na začiatok a používateľ môže zadať nové ID – namiesto toho, aby sa pokračovalo ďalej.
- Zabraňuje zbytočnému dotazu na potvrdenie alebo pokusu o vymazanie neexistujúceho úlohy.

if __name__ == "__main__": zabezpečuje, že sa daný blok kódu vykoná len vtedy, keď sa súbor spustí priamo, nie keď sa importuje.

Je to najlepší spôsob, ako oddeliť "spustenie aplikácie" od "definovania funkcií a logiky".