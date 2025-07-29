import pymysql
import pytest
from Projekt_2.db_config import DB_CONFIG, create_connection
from Projekt_2.Test.Task_manager_TEST_SQL import create_table_if_not_exist, add_task_into_db, update_task_status_db, delete_task_input

@pytest.fixture(scope="session")
def conn():
    conn = create_connection()
    yield conn
    conn.close()

@pytest.fixture(scope="function")
def set_up_test(conn):
#"""Vytvorí testovaciu tabuľku pred každým testom a zmaže ju po teste."""
    # Setup – vytvorenie tabuľky
    create_table_if_not_exist(conn)
    yield conn  # poskytne conn do testu   

    # Teardown – zmazanie tabuľky
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS Ukoly_test;")
    conn.commit()
    cursor.close()

#!!!!!!!!!! UPRAVIT FIXTURE 

# --------- test pro PRIDANI UKOLU ---------

@pytest.mark.parametrize("nazev_ukolu, popis_ukolu", [
    ("Test 1", "Ukol pro input"),
    ("Dlhy nazov *3", "dlhsi popis *10"),
    ("a", "B"),
    (" medzery.    ", "   kvoli strip     ")
])
def test_add_task_positive_par(conn, nazev_ukolu, popis_ukolu):
    vysledok = add_task_into_db(conn, nazev_ukolu, popis_ukolu)
    if vysledok:
        print("podla ocakavani ulozena uloha")
    assert vysledok, "❌ Chyba: Úloha sa neuložila, aj keď vstupy boli platné."

 # skontrolujem, ze sa uloha ulozila
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(
        "SELECT nazev, popis FROM Ukoly_test WHERE nazev = %s AND popis = %s",
        (nazev_ukolu.strip(),popis_ukolu.strip())
    )
    new_task = cursor.fetchone()
    if new_task:
        print("✅ Spravne ulozenie novej ulohy pri zadanych vstupoch")
    
    assert new_task is not None, f"❌ Úloha s názvom '{nazev_ukolu}' sa nenašla v DB."
    assert new_task["nazev"] == nazev_ukolu.strip(), f"❌ Necakana chyba pri spravnom zadani vstupov"



@pytest.mark.parametrize("nazev_ukolu, popis_ukolu", [
    ("", "Platný popis"),          # prázdny názov
    ("   ", "Platný popis"),       # len medzery v názve
    ("Platný název", ""),          # prázdny popis
    ("Platný název", "   "),       # len medzery v popise
    ("", ""),                      # oba prázdne
    ("   ", "   "),                # oba whitespace
])
def test_add_task_negative(conn, nazev_ukolu, popis_ukolu):
    with pytest.raises(ValueError, match="Název a popis úkolu jsou povinné"):
        add_task_into_db(conn, nazev_ukolu, popis_ukolu)








# @pytest.mark.add
# def test_add_task_negative(conn):
#     nazev_ukolu = "Ukol2"
#     popis_ukolu = ""
#     with pytest.raises(ValueError):
#         add_task_into_db(conn,nazev_ukolu, popis_ukolu)
#     #kontrola
#     cursor = conn.cursor(pymysql.cursors.DictCursor)
#     cursor.execute(
#         "SELECT id, nazev, popis FROM Ukoly_test WHERE nazev =%s;",
#         ("Ukol2",)
#     ) 
#     result = cursor.fetchone()
#     if result is None:
#         print("✅ Ocavany vysledok je neulozenie ulohy, pretoze vyplnenie pola pre nazov a popis su povinne")
#     cursor.close()

#     assert result is None, f"❌ ocekavano None, ve skutecnosti {result}"


# if result is None:
#         print("✅ Uloha sa spravne neulozila, overenie povinych vstupov")




# @pytest.mark.add
# def test_add_task_positive(conn, create_table): 
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

# @pytest.mark.add
# def test_add_task_negative(conn,create_table):

#     with pytest.raises(ValueError):

#         add_task_into_sql(conn,nazev_ukolu="Ukol 2", popis_ukolu="")

#     cursor = conn.cursor(pymysql.cursors.DictCursor)
#     cursor.execute(
#         "SELECT id, nazev, popis FROM Ukoly_test WHERE nazev =%s;",
#         ("Ukol2",)
#     ) 
#     result = cursor.fetchone()
#     print("✅ Ocavany je vysledok je neulozenie ulohy, pretoze vyplnenie pola pre nazov a popis su povinne")
#     cursor.close()

#     assert result is None, f"❌ocekavano None, ve skutecnosti {result}"

# @pytest.mark.add
# def test_add_task_duplicity_negative(conn,create_table):
#     cursor = conn.cursor()
#     cursor.execute(
#         "INSERT INTO Ukoly_test (id, nazev, popis) VALUES (%s, %s, %s);",
#         (2901, "vlozenie id", "negativni test 1")
#     )
#     conn.commit()


#     with pytest.raises(pymysql.err.IntegrityError):
#         cursor.execute(
#             "INSERT INTO Ukoly_test (id, nazev, popis) VALUES (%s, %s, %s);",
#             (2901, "duplicitne id", "negativni test 2")
#         )
#         conn.commit()

#     if pytest.raises:
#         print(f"✅ nepoovolene duplicitne zadanie id")
#     cursor.close()

# @pytest.mark.add
# def test_insert_invalid_data_negative(conn,create_table):
#     cursor=conn.cursor()

#     with pytest.raises(pymysql.err.DataError,  match="Data too long for column"):
#         cursor.execute("INSERT INTO Ukoly_test (nazev, popis) VALUES (%s, %s)", ('a' * 101, 'vlozenie retazca o dlzke nad povoleny vstup'))
#         conn.commit()

#         cursor.close()

# #------------- testy na AKTUALIZOVAT UKOL -------
# @pytest.mark.update
# def test_update_data_positive(conn,create_table):
    
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO Ukoly_test (nazev, popis) VALUES ('update ukolu', 'funkcia skusa spravnu aktualizaciu tabulky');")
#     conn.commit()

#     cursor.execute("UPDATE Ukoly_test SET stav = 'Hotovo' WHERE nazev = 'update ukolu';")
#     conn.commit()

#     cursor.execute("SELECT * FROM Ukoly_test WHERE nazev = 'update ukolu';")
#     result = cursor.fetchone()
#     cursor.close()
#     print(result)
#     assert result[3] == "Hotovo", "Stav nebyl správně aktualizován."

# @pytest.mark.update
# def test_get_task_id_positive(conn,create_table):
#     cursor=conn.cursor()
#     cursor.execute(
#         "INSERT INTO Ukoly_test (nazev, popis) VALUES ('ukol pro get task id', 'vytvorenie ulohy, aby zoznam nikdy nebol prazdny');"
#         )
#     conn.commit()
        
#     nove_id = cursor.lastrowid
#     cursor.close()

#     if nove_id:
#         print(f"✅ nove_id vlozenej ulohy je: {nove_id}")

#     result = get_task_id(conn, nove_id)
#     assert result == nove_id, f"❌ Očakávané ID {nove_id}, ale vrátené: {result}"

# @pytest.mark.update
# def test_get_task_id_negative(conn,create_table):
#     neexistujuce_id = 999999

#     result = get_task_id(conn, neexistujuce_id)
#     assert result is None

# @pytest.mark.update
# def test_get_task_id_2_negative(conn,create_table):
#     cursor = conn.cursor(pymysql.cursors.DictCursor) 
#     cursor.execute("SELECT id FROM Ukoly_test ORDER BY id DESC LIMIT 1;")
#     max_id = cursor.fetchone()
#     cursor.close()
     
#     if max_id:
#         vyber = max_id["id"]
#     else:
#         vyber = 0

#     up_max_id = vyber + 1000

#     result = get_task_id(conn, up_max_id)
#     if result is None:
#         print(f"✅ Zadane id: {up_max_id} neexistuje podla ocakavania")

#     assert result is None, f"❌ Očakávané 'None' pre ID {max_id}, ale vrátené: {result}"


# @pytest.mark.update
# def test_kontrola_id_status_positive(conn,create_table): #funkcia v kode vracia True ak sa nachazda v tabulke a  false ak nenajde take id

#     cursor=conn.cursor()
#     cursor.execute(
#         "INSERT INTO Ukoly_test (nazev, popis) VALUES ('ukol pre kontrolu id statusu', 'vytvorenie ulohy, aby sme zistili jej id, a aby zoznam nidy nebol prazdny');"
#         )
#     conn.commit()
        
#     nove_id = cursor.lastrowid  
#     cursor.close()

#     result = kontrola_id_status(conn, nove_id)

#     assert result is True, f"❌ Očakávané True pre existujúce ID {nove_id}, vrátené: {result}"

# @pytest.mark.update
# def test_kontrola_id_status_negative(conn,create_table):
#     neexistujuce_id= -1
#     result = kontrola_id_status(conn, neexistujuce_id)

#     assert result is False, f"❌ Očakávané False pre zaporne ID, vrátené: {result}"

# @pytest.mark.update
# def test_update_task_status_get_id_positive(conn,create_table):
#     zadanie_stavu = "Probíhá"

#     cursor=conn.cursor()
#     cursor.execute(
#         "INSERT INTO Ukoly_test (nazev, popis) VALUES ('ukol pre kontrolu update ulohy', 'vytvorenie ulohy, aby sme zistili jej id, a ci ju funkcia vyhodnoti spravne podla ocakavania');"
#         )
#     conn.commit()
        
#     nove_id = cursor.lastrowid  

#     result = update_task_status (conn, nove_id, zadanie_stavu)
    
#     assert result is True, f"❌ Očakávané True, zadali sme povoleny stav, hlasi {result}"

# @pytest.mark.update  
# def test_update_task_status_get_id_positive(conn,create_table):
#     zadanie_stavu = "Hotovo"

#     cursor=conn.cursor()
#     cursor.execute(
#         "INSERT INTO Ukoly_test (nazev, popis) VALUES ('ukol pre kontrolu id statusu', 'vytvorenie ulohy, aby sme zistili jej id, pre aktualizaciu stavu');"
#         )
#     conn.commit()
        
#     nove_id = cursor.lastrowid

#     result = update_task_status (conn, nove_id, zadanie_stavu)
#     print(result)
#     assert result is True, f"❌ Očakávané True, zadali sme povoleny stav, hlasi {result}"

#     cursor = conn.cursor()
#     cursor.execute(
#     "SELECT id, nazev, stav FROM Ukoly_test WHERE id=%s;",
#     (nove_id,)
#     )
#     skuska = cursor.fetchone()
#     print(skuska)

# @pytest.mark.update
# def test_update_task_status_get_id_negative(conn,create_table):
#     zadanie_stavu = "Nevim"

#     cursor=conn.cursor()
#     cursor.execute(
#         "INSERT INTO Ukoly_test (nazev, popis) VALUES ('ukol pre kontrolu id statusu 2', 'vytvorenie ulohy, aby sme zistili jej id, pre negativne testovanie');"
#         )
#     conn.commit()
        
#     nove_id = cursor.lastrowid
#     cursor.close()

#     with pytest.raises(ValueError, match="Neplatný stav úkolu"):
#         update_task_status (conn, nove_id, zadanie_stavu)
        
    
#     # poznamka pre mna: assert sa nepouzije, lebo funkcia nema co vratit, vyhodi vynimnku

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