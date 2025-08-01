import pymysql
import pytest
from Projekt_2.db_config import DB_CONFIG, create_connection
from Projekt_2.Test.Task_manager_TEST_SQL import add_task_into_db, update_task_status_db, delete_task_by_id, get_all_tasks_from_db, check_task_id

# zavolam create connection, pretoze ta je v db config. 

@pytest.fixture(scope="session")
def conn():
    conn = create_connection()
    print("Vytváram databázové pripojenie.")
    yield conn

    print("Zatváram databázové pripojenie.")
    conn.close()

@pytest.fixture(scope="function")
def set_up_test(conn):
#"""Vytvorí testovaciu tabuľku pred každým testom a zmaže ju po teste."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Ukoly_test (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nazev VARCHAR(50) NOT NULL,
            popis VARCHAR(255) NOT NULL,
            stav ENUM('Nezahájeno', 'Probíhá', 'Hotovo') NOT NULL DEFAULT 'Nezahájeno',
            datum_vytvoreni DATE DEFAULT (CURRENT_DATE)
        );
    """)
    conn.commit()
    print("tabulka pripravena")
    yield cursor
    print("som za fixture pre tabulku")

    # Teardown – zmazanie tabuľky
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS Ukoly_test;")
    conn.commit()
    print("Testovacia tabuľka bola zmazaná.\n")
    cursor.close()

# #!!!!!!!!!! UPRAVIT FIXTURE 

# # # --------- test pro PRIDANI UKOLU ---------

@pytest.mark.parametrize("nazev_ukolu, popis_ukolu", [
    ("Test 1", "Ukol pro input"),
    ("Dlhy nazov *2", "dlhsi popis *3"),
    ("a", "B"),
    (" medzery.    ", "   kvoli strip     ")
])
@pytest.mark.add
def test_add_task_unit_param_positive(conn, set_up_test, nazev_ukolu, popis_ukolu):
    vysledok = add_task_into_db(conn, nazev_ukolu, popis_ukolu)
    if vysledok:
        print(f"podla ocakavani ulozena uloha: {vysledok}")
        print("SOM V TESTE")
    assert vysledok == True, "❌ Chyba: Úloha sa neuložila, aj keď vstupy boli platné."

 # skontrolujem, ze sa uloha ulozila
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(
        "SELECT nazev, popis FROM Ukoly_test WHERE nazev = %s AND popis = %s",
        (nazev_ukolu.strip(),popis_ukolu.strip())
    )
    new_task = cursor.fetchone()
    cursor.close()
    if new_task:
        print("✅ Spravne ulozenie novej ulohy pri zadanych vstupoch")
        print(f"TATO ULOHA: {new_task}")
    
    assert new_task is not None, f"❌ Úloha s názvom '{nazev_ukolu}' sa nenašla v DB."
    assert new_task["nazev"] == nazev_ukolu.strip(), f"❌ Úloha '{nazev_ukolu}' sa nenašla medzi výsledkami."
    assert new_task["popis"] == popis_ukolu.strip()


@pytest.mark.parametrize("nazev_ukolu, popis_ukolu", [
    ("", "Platný popis"),          # prázdny názov
    ("   ", "Platný popis"),       # len medzery v názve
    ("Platný název", ""),          # prázdny popis
    ("Platný název", "   "),       # len medzery v popise
    ("", ""),                      # oba prázdne
    ("   ", "   ")                 # oba whitespace
])
@pytest.mark.add
def test_add_task_unit_param_negative(conn, set_up_test, nazev_ukolu, popis_ukolu):
    with pytest.raises(ValueError, match="Název a popis úkolu jsou povinné"):
        add_task_into_db(conn, nazev_ukolu, popis_ukolu)
#kontrola
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(
        "SELECT id, nazev, popis FROM Ukoly_test WHERE nazev =%s;",
        (nazev_ukolu,)
    ) 
    result = cursor.fetchone()
    if result is None:
        print("✅ Ocavany vysledok je neulozenie ulohy, pretoze vyplnenie pola pre nazov a popis su povinne")
    cursor.close()

    assert result is None, f"❌ ocekavano None, ve skutecnosti {result}"

@pytest.mark.add
def test_add_task_invalid_data_negative(conn,set_up_test):
    cursor=conn.cursor()

    with pytest.raises(pymysql.err.DataError,  match="Data too long for column"):
        cursor.execute("INSERT INTO Ukoly_test (nazev, popis) VALUES (%s, %s)", ("a" * 101, "vlozenie retazca o dlzke nad povoleny vstup" * 100))
        conn.commit()
        cursor.close()


@pytest.mark.add
def test_add_task_integračný_positive(conn,set_up_test):
    nazev_ukolu="integracni test"
    popis_ukolu="overenie add_task pouzitim oboch funkcii"

    vysledok = add_task_into_db(conn, nazev_ukolu, popis_ukolu)
    assert vysledok == True

    zoznam = get_all_tasks_from_db(conn)

    for task in zoznam:
        if task["nazev"] == nazev_ukolu:
            print(task)

    assert task["nazev"] == "integracni test"
    assert task["popis"] == "overenie add_task pouzitim oboch funkcii"
    assert task is not None, f"❌ Necakana reakcia testu pri ukladani spravnych vstupov"
    assert any(task["nazev"] == nazev_ukolu and task["popis"] == popis_ukolu for task in zoznam), f"❌ Úloha '{nazev_ukolu}' nebola nájdená v DB."



#------ UPDATE UKOLU
@pytest.mark.parametrize("novy_stav", [
    ("Probíhá"),          
    ("Hotovo")
])
@pytest.mark.update
def test_update_task_status_db_positive(conn,set_up_test, novy_stav):
    cursor=conn.cursor()
    cursor.execute(
        "INSERT INTO Ukoly_test (nazev, popis) VALUES ('ukol pro update', 'vytvorenie ulohy, aby zoznam nikdy nebol prazdny');"
        )
    conn.commit()
        
    nove_id = cursor.lastrowid
    cursor.close()

    # zavolame funkciu, pouzijeme nove id, zmenime stav spravnou hodnotou. 
    result = update_task_status_db(conn, vyber_id=nove_id, novy_stav=novy_stav)

    assert result["id"] == nove_id
    assert result["stav"] == novy_stav
    assert result["nazev"] == "ukol pro update"
    assert result is not None, "Ocakavame novu updatovanu ulohu, ale vysledok nenalezen"


@pytest.mark.parametrize("novy_stav", [
    ("Rozpracované "),       
    (1),
    ("")
])
def test_update_task_status_db_negative(conn, set_up_test, novy_stav):
    cursor=conn.cursor()
    cursor.execute(
        "INSERT INTO Ukoly_test (nazev, popis) VALUES ('ukol pro update 2', 'vytvorenie ulohy, aby zoznam nikdy nebol prazdny');"
        )
    conn.commit()
        
    nove_id = cursor.lastrowid
    cursor.close()

    # zavolame funkciu, pouzijeme nove id, zmenime stav na neplatnu hodnotou - raise error
    with pytest.raises(ValueError, match="Neplatný stav."):
        update_task_status_db(conn, vyber_id=nove_id, novy_stav=novy_stav)

    # Overenie, že sa stav naozaj nezmenil
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(
        "SELECT nazev, stav FROM Ukoly_test WHERE id = %s;",
        (nove_id,)
    )
    updated_task = cursor.fetchone()
    cursor.close()

    assert updated_task["stav"] != novy_stav, "Stav by sa nemal zmeniť na neplatnú hodnotu, moze mat len Hotovo/Probíhá."
   

@pytest.mark.update
def test_update_task_status_id_negative(conn, set_up_test):
    #dobry stav, zle id
    novy_stav = "Probíhá"
    vyber_id = -1
    result = update_task_status_db(conn, vyber_id, novy_stav)
    
    assert result is None, f"❌ Očakávané None, ale hlasi {result}"


# CHECK TASK ID PRI UPDATE
@pytest.mark.update
def test_check_task_id_positive(conn, set_up_test):
    cursor=conn.cursor()
    cursor.execute(
        "INSERT INTO Ukoly_test (nazev, popis) VALUES ('ukol pro get task id', 'vytvorenie ulohy, aby zoznam nikdy nebol prazdny');"
        )
    conn.commit()
        
    nove_id = cursor.lastrowid
    cursor.close()

    result = check_task_id(conn,nove_id)
    if result:
        print(f"✅ nove_id vlozenej ulohy je: {nove_id}")

    assert result == True, f"❌ Očakávané ID {nove_id}, ale neznama chyba"



@pytest.mark.parametrize("vyber_id", [
    (0),          
    (-1),       
    (99999)
])
@pytest.mark.update
def test_check_task_id_negative(conn, set_up_test, vyber_id):

    result = check_task_id(conn,vyber_id=vyber_id)
    if result is False:
        print("spravne False pre neexistujuce id")

    assert result == False


#------ DELETE UKOLU
@pytest.mark.delete
def test_delete_task_positive(conn, set_up_test):
    cursor=conn.cursor()
    cursor.execute(
        "INSERT INTO Ukoly_test (nazev, popis) VALUES ('mazanie ulohy', 'uhola pre zmazanie podla id');"
    )
    conn.commit()
    nove_id = cursor.lastrowid

    result = delete_task_by_id(conn, task_id=nove_id)

    assert result == True


@pytest.mark.parametrize("not_exist_id", [
    (0),
    (-1),
    (999999)                                
])
@pytest.mark.delete
def test_delete_task_negative(conn, set_up_test, not_exist_id):


    result = delete_task_by_id(conn, task_id=not_exist_id)
    assert result == False, f"Ocakavame false, vysledok: {result}"



# ------------- NAVIAC test na ZOBRAZIT UKOLY ------- 
def test_get_all_tasks_positive(conn, set_up_test):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Ukoly_test (nazev, popis) VALUES ('ukol pro seznam', 'vytvoreni ukol aby seznam nebyl nikdy prazdny');"
    )
    conn.commit()
    cursor.close()

    tasks = get_all_tasks_from_db(conn)

    # overíme, že výsledok je list a nie je prázdny
    assert isinstance(tasks, list), "Očakávame, že get_all_tasks_from_db vráti list"
    assert len(tasks) > 0, "Očakávame aspoň jeden záznam v zozname"

# skuska
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(
        "SELECT * FROM Ukoly_test WHERE nazev = %s;",
        ('ukol pro seznam',)
    )
    skuska = cursor.fetchone()
    cursor.close()

    assert skuska is not None, "Očakávame, že záznam v tabuľke existuje"
    assert skuska["nazev"] == "ukol pro seznam"


    assert "id" in tasks[0]
    assert "nazev" in tasks[0]



def test_get_all_tasks_negative(conn, set_up_test):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Ukoly_test;")
    conn.commit()
    cursor.close()

    tasks = get_all_tasks_from_db(conn)
    if tasks is None:
        print("✅ Zoznam je prazdny podla ocakavania")

    assert not tasks, f"Ocakavame prazdny zoznam, ale {tasks}"