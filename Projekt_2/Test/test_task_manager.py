import pymysql
import pytest
from Projekt_2.db_config import DB_CONFIG, create_connection
from Projekt_2.Test.Task_manager_TEST_SQL import create_table_if_not_exist, add_task_into_db, update_task_status_db, delete_task_input, get_all_tasks_from_db, check_task_id

@pytest.fixture(scope="session")
def conn():
    conn = create_connection()
    yield conn
    conn.close()

@pytest.fixture(scope="function")
def set_up_test(conn):
#"""Vytvorí testovaciu tabuľku pred každým testom a zmaže ju po teste."""
    create_table_if_not_exist(conn)
    yield conn  # poskytne conn do testu   

    # Teardown – zmazanie tabuľky
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS Ukoly_test;")
    conn.commit()
    cursor.close()

#!!!!!!!!!! UPRAVIT FIXTURE 

# # --------- test pro PRIDANI UKOLU ---------

@pytest.mark.parametrize("nazev_ukolu, popis_ukolu", [
    ("Test 1", "Ukol pro input"),
    ("Dlhy nazov *2", "dlhsi popis *3"),
    ("a", "B"),
    (" medzery.    ", "   kvoli strip     ")
])
@pytest.mark.add
def test_add_task_unit_param_positive(conn, nazev_ukolu, popis_ukolu):
    vysledok = add_task_into_db(conn, nazev_ukolu, popis_ukolu)
    if vysledok:
        print("podla ocakavani ulozena uloha")
    assert vysledok == True, "❌ Chyba: Úloha sa neuložila, aj keď vstupy boli platné."

 # skontrolujem, ze sa uloha ulozila
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(
        "SELECT nazev, popis FROM Ukoly_test WHERE nazev = %s AND popis = %s",
        (nazev_ukolu.strip(),popis_ukolu.strip())
    )
    new_task = cursor.fetchall()
    cursor.close()
    if new_task:
        print("✅ Spravne ulozenie novej ulohy pri zadanych vstupoch")
    
    assert new_task is not None, f"❌ Úloha s názvom '{nazev_ukolu}' sa nenašla v DB."
    assert any(task["nazev"] == nazev_ukolu.strip() and task["popis"] == popis_ukolu.strip()
        for task in new_task), f"❌ Úloha '{nazev_ukolu}' sa nenašla medzi výsledkami."



@pytest.mark.parametrize("nazev_ukolu, popis_ukolu", [
    ("", "Platný popis"),          # prázdny názov
    ("   ", "Platný popis"),       # len medzery v názve
    ("Platný název", ""),          # prázdny popis
    ("Platný název", "   "),       # len medzery v popise
    ("", ""),                      # oba prázdne
    ("   ", "   ")                 # oba whitespace
])
@pytest.mark.add
def test_add_task_unit_param_negative(conn, nazev_ukolu, popis_ukolu):
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
def test_add_task_invalid_data_negative(conn):
    cursor=conn.cursor()

    with pytest.raises(pymysql.err.DataError,  match="Data too long for column"):
        cursor.execute("INSERT INTO Ukoly_test (nazev, popis) VALUES (%s, %s)", ("a" * 101, "vlozenie retazca o dlzke nad povoleny vstup" * 100))
        conn.commit()
        cursor.close()


@pytest.mark.add
def test_add_task_integračný_positive(conn):
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
def test_update_task_status_db_positive(conn, novy_stav):
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
def test_update_task_status_db_negative(conn,novy_stav):
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
def test_update_task_status_id_negative(conn):
    #dobry stav, zle id
    novy_stav = "Probíhá"
    vyber_id = -1
    result = update_task_status_db(conn, vyber_id, novy_stav)
    
    assert result is None, f"❌ Očakávané None, ale hlasi {result}"

# CHECK TASK ID PRI UPDATE
@pytest.mark.update
def test_check_task_id_positive(conn):
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
def test_check_task_id_negative(conn,vyber_id):

    result = check_task_id(conn,vyber_id)
    if result is False:
        print("spravne False pre neexistujuce id")

    assert result == False



#///////////////////////////////////////////////////////////////







# # ------------- testy na ODSTRANENIE UKOLU -------
# @pytest.mark.delete
# def test_delete_task_by_id_positive(conn,create_table): #vrati T/F
#     cursor=conn.cursor()
#     cursor.execute(
#         "INSERT INTO Ukoly_test (nazev, popis) VALUES ('mazanie ulohy', 'uhola pre zmazanie podla id');"
#         )
#     conn.commit()
#     nove_id = cursor.lastrowid

#     cursor.execute(
#         "SELECT * FROM Ukoly_test WHERE id=%s;",
#             (nove_id)
#         )
#     skuska = cursor.fetchone()
#     cursor.close()
#     print(f"Vyvorili sme skusku: {skuska}")

#     result = delete_task_by_id(conn, nove_id)
#     assert result is True, f"❌  ocakavme true, ze sa uloha zmaze a vyslo {result}"


# @pytest.mark.delete
# def test_delete_task_by_id_negative(conn,create_table):
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM Ukoly_test WHERE id=-1;")
#     conn.commit()

#     result = delete_task_by_id(conn, task_id=-1)
#     assert result == False, f"❌  ocakavme False pri zapornom id a vyslo {result}"

# @pytest.mark.delete
# def test_delete_data_positive(conn,create_table):
#     cursor=conn.cursor()

#     cursor.execute("INSERT INTO Ukoly_test (nazev, popis) VALUES ('vlozenie pre delete', 'touto uohou si overime, ci sa po zmazani uz nenachadza v zozname')")
#     conn.commit()

#     cursor.execute("SELECT * FROM Ukoly_test WHERE nazev = 'vlozenie pre delete'")
#     skuska = cursor.fetchone()
#     print(skuska)

#     cursor.execute("DELETE FROM Ukoly_test WHERE nazev = 'vlozenie pre delete'")
#     conn.commit()


#     cursor.execute("SELECT * FROM Ukoly_test WHERE nazev = 'vlozenie pre delete'")
#     result = cursor.fetchone()
#     cursor.close()
#     assert result is None, "Záznam nebyl správně smazán."

# # ------------- NAVIAC test na ZOBRAZIT UKOLY ------- 
# def test_get_all_tasks_positive(conn,create_table):
#     cursor=conn.cursor()
#     cursor.execute(
#         "INSERT INTO Ukoly_test (nazev, popis) VALUES ('ukol pro seznam', 'vytvoreni ukol aby seznam nebyl nikdy prazdny');"
#         )
#     conn.commit()

#     tasks = get_all_tasks(conn)
#     if tasks is not None:
#         print("✅ Tabulka zobrazuje ulohy")

#     cursor.execute(
#         "SELECT * FROM Ukoly_test WHERE nazev='ukol pro seznam';")
#     skuska = cursor.fetchone()

#     assert len(tasks) > 0  
#     assert "id" in tasks[0]
#     assert "nazev" in tasks[0]
#     assert tasks is not None, f"❌ ocekavany zaznam v tabulke, v skutocnosti zoznam prazdny"

#     assert skuska[1] == "ukol pro seznam"


# def test_get_all_tasks_negative(conn,create_table):
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM Ukoly_test;")
#     conn.commit()
#     cursor.close()

#     tasks = get_all_tasks(conn)
#     if tasks is None:
#         print("✅ Zoznam je prazdny podla ocakavania")

#     assert tasks == None