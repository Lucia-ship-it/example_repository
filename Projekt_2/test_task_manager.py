import pymysql
import pytest
from Projekt_2.Task_manager_TEST_SQL import add_task_overenie_input, add_task_into_sql, get_task_id, kontrola_id_status, update_task_status, delete_task_by_id, get_all_tasks

#-!!! ZADANIE: Testy ověří správnou funkčnost operací přidání, aktualizace a odstranění úkolů pomocí pytest.

#pri command not found:
# ls
# python3 -m venv venv
# source venv/bin/activate
# pip install pytest
# pytest
# pip show pymysql
# which python
# source venv/bin/activate
# pip install pymysql

# idealne spustit cez: pytest -s -v

@pytest.fixture
def conn():
    connection = pymysql.connect(
                    host="mysql80.r4.websupport.sk",
                    port=3314,
                    user="EsPMMROq",
                    password="79_|rBg[1F=`}cj|I%kc",
                    database="Task_manager_SQL"            
                )

    cursor = connection.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS Ukoly_test (
                id INT PRIMARY KEY AUTO_INCREMENT,
                nazev VARCHAR(50) NOT NULL,
                popis VARCHAR(255) NOT NULL,
                stav ENUM('Nezahájeno', 'Probíhá', 'Hotovo') NOT NULL DEFAULT 'Nezahájeno',
                datum_vytvoreni DATE DEFAULT (CURRENT_DATE)
            );
    """)
    connection.commit()

    # Předání připojení a kurzoru testům
    yield connection # ⬅️ tu vraciaš pripojenie testom

        # Úklid po testech: Smazání tabulky
    cursor.execute("DROP TABLE IF EXISTS Ukoly_test")
    connection.commit()

    # Uzavření připojení
    cursor.close()
    connection.close()


# --------- test pro PRIDANI UKOLU ---------
@pytest.mark.add
def test_add_task_overenie_input_positive(conn):
    result = add_task_overenie_input(nazev_ukolu="ukol pro input", popis_ukolu="overenie funkcnosti string vstupu")
    if result is not None:
        print("✅ Spravne overenie zadanych vstupov")
    assert result, f"❌ Necakana chyba pri spravnom zadani nazvu a popisu" 

@pytest.mark.add
def test_add_task_overenie_input_negative(conn):
    result = add_task_overenie_input(nazev_ukolu="ukol pro input", popis_ukolu="")
    if result is None:
        print("✅ Spravne overenie nevyplnenych vstupov")

    assert result is None, f"❌ Zapisuje ukol aj pri prazdnom vstupe" 

# @pytest.mark.add
# def test_add_task_positive(conn): 
#     add_task_into_sql(conn,nazev_ukolu="ulozenie ulohy do tabulky", popis_ukolu="overenie, ze test vytvori ulohu v tabulke")
    
#     cursor = conn.cursor(pymysql.cursors.DictCursor)
#     cursor.execute(# overime, ci tam je
#         "SELECT id, nazev, popis FROM Ukoly_test WHERE nazev =%s;",
#         ("ulozenie ulohy do tabulky",)
#     ) 
#     result = cursor.fetchone()
#     print(result)
#     print("✅ Uloha sa uklada podla ocakavnia")
#     cursor.close()

#     assert result["nazev"] == "ulozenie ulohy do tabulky"
#     assert result["popis"] == "overenie, ze test vytvori ulohu v tabulke"
#     assert result is not None, f"❌ Necakana reakcia testu pri ukladani spravnych vstupov"

@pytest.mark.add
def test_add_task_negative(conn):

    with pytest.raises(ValueError):

        add_task_into_sql(conn,nazev_ukolu="Ukol 2", popis_ukolu="")

    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(
        "SELECT id, nazev, popis FROM Ukoly_test WHERE nazev =%s;",
        ("Ukol2",)
    ) 
    result = cursor.fetchone()
    print("✅ Ocavany je vysledok je neulozenie ulohy, pretoze vyplnenie pola pre nazov a popis su povinne")
    cursor.close()

    assert result is None, f"❌ocekavano None, ve skutecnosti {result}"

@pytest.mark.add
def test_add_task_duplicity_negative(conn):
    cursor = conn.cursor()
# program umozni zadat mno urcene id, ale kedze mame yield, neostane v tabulke. preto to musim pridat v jednom kroku rovno druhy krat
    cursor.execute(
        "INSERT INTO Ukoly_test (id, nazev, popis) VALUES (%s, %s, %s);",
        (2901, "vlozenie id", "negativni test 1")
    )
    conn.commit()


    with pytest.raises(pymysql.err.IntegrityError):
        cursor.execute(
            "INSERT INTO Ukoly_test (id, nazev, popis) VALUES (%s, %s, %s);",
            (2901, "duplicitne id", "negativni test 2")
        )
        conn.commit()

    if pytest.raises:
        print(f"✅ nepoovolene duplicitne zadanie id")
    cursor.close()

@pytest.mark.add
def test_insert_invalid_data_negative(conn):#zo skript
    cursor=conn.cursor()

    # Pokus o vložení příliš dlouhého textu
    with pytest.raises(pymysql.err.DataError,  match="Data too long for column"):
        cursor.execute("INSERT INTO Ukoly_test (nazev, popis) VALUES (%s, %s)", ('a' * 101, 'vlozenie retazca o dlzke nad povoleny vstup'))
        conn.commit()

        cursor.close()

#------------- testy na AKTUALIZOVAT UKOL -------
@pytest.mark.update
def test_update_data_positive(conn): #zo skript
    
    cursor = conn.cursor()
    # Vložení testovacího záznamu
    cursor.execute("INSERT INTO Ukoly_test (nazev, popis) VALUES ('update ukolu', 'funkcia skusa spravnu aktualizaciu tabulky');")
    conn.commit()

    # Aktualizace dat
    cursor.execute("UPDATE Ukoly_test SET stav = 'Hotovo' WHERE nazev = 'update ukolu';")
    conn.commit()

    # Ověření aktualizace
    cursor.execute("SELECT * FROM Ukoly_test WHERE nazev = 'update ukolu';")
    result = cursor.fetchone()
    cursor.close()
    print(result)
    assert result[3] == "Hotovo", "Stav nebyl správně aktualizován."

@pytest.mark.update
def test_get_task_id_positive(conn):
    cursor=conn.cursor()
    cursor.execute(
        "INSERT INTO Ukoly_test (nazev, popis) VALUES ('ukol pro get task id', 'vytvorenie ulohy, aby zoznam nikdy nebol prazdny');"
        )
    conn.commit()
        
    # Získame ID posledne vloženého záznamu
    nove_id = cursor.lastrowid  # ⬅️ Lepšie ako "SELECT * FROM Ukoly_test ORDER BY id DESC LIMIT 1;"
    cursor.close()

    if nove_id:
        print(f"✅ nove_id vlozenej ulohy je: {nove_id}")

    result = get_task_id(conn, nove_id)
    assert result == nove_id, f"❌ Očakávané ID {nove_id}, ale vrátené: {result}"

@pytest.mark.update
def test_get_task_id_negative(conn):
    neexistujuce_id = 999999

    result = get_task_id(conn, neexistujuce_id)
    assert result is None

@pytest.mark.update
def test_get_task_id_2_negative(conn):
    cursor = conn.cursor(pymysql.cursors.DictCursor) #aby si vedel vybrat kluc
    cursor.execute("SELECT id FROM Ukoly_test ORDER BY id DESC LIMIT 1;")
    max_id = cursor.fetchone()
    cursor.close()
     
    if max_id:
        vyber = max_id["id"]
    else:
        vyber = 0

    up_max_id = vyber + 1000 #aby sme mali 100% istotu

    result = get_task_id(conn, up_max_id)
    if result is None:
        print(f"✅ Zadane id: {up_max_id} neexistuje podla ocakavania")

    assert result is None, f"❌ Očakávané 'None' pre ID {max_id}, ale vrátené: {result}"


@pytest.mark.update
def test_kontrola_id_status_positive(conn): #funkcia v kode vracia True ak sa nachazda v tabulke a  false ak nenajde take id

    cursor=conn.cursor()
    cursor.execute(
        "INSERT INTO Ukoly_test (nazev, popis) VALUES ('ukol pre kontrolu id statusu', 'vytvorenie ulohy, aby sme zistili jej id, a aby zoznam nidy nebol prazdny');"
        )
    conn.commit()
        
    nove_id = cursor.lastrowid  
    cursor.close()

    result = kontrola_id_status(conn, nove_id)

    assert result is True, f"❌ Očakávané True pre existujúce ID {nove_id}, vrátené: {result}"

@pytest.mark.update
def test_kontrola_id_status_negative(conn):
    neexistujuce_id= -1
    result = kontrola_id_status(conn, neexistujuce_id)

    assert result is False, f"❌ Očakávané False pre zaporne ID, vrátené: {result}"

@pytest.mark.update
def test_update_task_status_get_id_positive(conn):
    zadanie_stavu = "Probíhá"

    cursor=conn.cursor()
    cursor.execute(
        "INSERT INTO Ukoly_test (nazev, popis) VALUES ('ukol pre kontrolu update ulohy', 'vytvorenie ulohy, aby sme zistili jej id, a ci ju funkcia vyhodnoti spravne podla ocakavania');"
        )
    conn.commit()
        
    nove_id = cursor.lastrowid  

    result = update_task_status (conn, nove_id, zadanie_stavu)
    
    assert result is True, f"❌ Očakávané True, zadali sme povoleny stav, hlasi {result}"

@pytest.mark.update  
def test_update_task_status_get_id_positive(conn):
    zadanie_stavu = "Hotovo"

    cursor=conn.cursor()
    cursor.execute(
        "INSERT INTO Ukoly_test (nazev, popis) VALUES ('ukol pre kontrolu id statusu', 'vytvorenie ulohy, aby sme zistili jej id, pre aktualizaciu stavu');"
        )
    conn.commit()
        
    nove_id = cursor.lastrowid

    result = update_task_status (conn, nove_id, zadanie_stavu)
    print(result)
    assert result is True, f"❌ Očakávané True, zadali sme povoleny stav, hlasi {result}"

    cursor = conn.cursor()
    cursor.execute(
    "SELECT id, nazev, stav FROM Ukoly_test WHERE id=%s;",
    (nove_id,)
    )
    skuska = cursor.fetchone()
    print(skuska)

@pytest.mark.update
def test_update_task_status_get_id_negative(conn):
    zadanie_stavu = "Nevim"

    cursor=conn.cursor()
    cursor.execute(
        "INSERT INTO Ukoly_test (nazev, popis) VALUES ('ukol pre kontrolu id statusu 2', 'vytvorenie ulohy, aby sme zistili jej id, pre negativne testovanie');"
        )
    conn.commit()
        
    nove_id = cursor.lastrowid
    cursor.close()

    with pytest.raises(ValueError, match="Neplatný stav úkolu"):
        update_task_status (conn, nove_id, zadanie_stavu)
        
    
    #poznamka pre mna: assert sa nepouzije, lebo funkcia nema co vratit, vyhodi vynimnku

# ------------- testzy na ODSTRANENIE UKOLU -------
@pytest.mark.delete
def test_delete_task_by_id_positive(conn): #vrati T/F
    cursor=conn.cursor()
    cursor.execute(
        "INSERT INTO Ukoly_test (nazev, popis) VALUES ('mazanie ulohy', 'uhola pre zmazanie podla id');"
        )
    conn.commit()
    nove_id = cursor.lastrowid

    cursor.execute(
        "SELECT * FROM Ukoly_test WHERE id=%s;",
            (nove_id)
        )
    skuska = cursor.fetchone()
    cursor.close()
    print(f"Vyvorili sme skusku: {skuska}")

    result = delete_task_by_id(conn, nove_id)
    assert result is True, f"❌  ocakavme true, ze sa uloha zmaze a vyslo {result}"


@pytest.mark.delete
def test_delete_task_by_id_negative(conn):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Ukoly_test WHERE id=-1;")
    conn.commit()

    result = delete_task_by_id(conn, task_id=-1)
    assert result == False, f"❌  ocakavme False pri zapornom id a vyslo {result}"

def test_delete_data_positive(conn): #zo skript
    cursor=conn.cursor()

    # Vložení testovacího záznamu
    cursor.execute("INSERT INTO Ukoly_test (nazev, popis) VALUES ('vlozenie pre delete', 'touto uohou si overime, ci sa po zmazani uz nenachadza v zozname')")
    conn.commit()

    cursor.execute("SELECT * FROM Ukoly_test WHERE nazev = 'vlozenie pre delete'")
    skuska = cursor.fetchone()
    print(skuska)
    # Smazání záznamu
    cursor.execute("DELETE FROM Ukoly_test WHERE nazev = 'vlozenie pre delete'")
    conn.commit()

    # Ověření mazání
    cursor.execute("SELECT * FROM Ukoly_test WHERE nazev = 'vlozenie pre delete'")
    result = cursor.fetchone()
    cursor.close()
    assert result is None, "Záznam nebyl správně smazán."

# ------------- test na ZOBRAZIT UKOLY ------- pomylila som sa, ale ked uz boli vyrobene, necham ich tu. aspon som si to precvicila

def test_get_all_tasks_positive(conn):
    cursor=conn.cursor()
    cursor.execute(
        "INSERT INTO Ukoly_test (nazev, popis) VALUES ('ukol pro seznam', 'vytvoreni ukol aby seznam nebyl nikdy prazdny');"
        )
    conn.commit()

    tasks = get_all_tasks(conn)
    if tasks is not None:
        print("✅ Tabulka zobrazuje ulohy")

    cursor.execute(
        "SELECT * FROM Ukoly_test WHERE nazev='ukol pro seznam';")
    skuska = cursor.fetchone()

    assert len(tasks) > 0  # očakávame, že sú tam nejaké tasky
    assert "id" in tasks[0]
    assert "nazev" in tasks[0]
    assert tasks is not None, f"❌ ocekavany zaznam v tabulke, v skutocnosti zoznam prazdny"

    assert skuska[1] == "ukol pro seznam"


def test_get_all_tasks_negative(conn):
    #vycistime tabulku, aby sme zistili, ci reaguje na prazdny zoznam
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Ukoly_test;")
    conn.commit()
    cursor.close()

    tasks = get_all_tasks(conn)
    if tasks is None:
        print("✅ Zoznam je prazdny podla ocakavania")

    assert tasks is None
    
#poznamky pre mna: fetchall vracia vzdy list [], nie tuple() -> [{"id": 1, "nazev": "..."}]