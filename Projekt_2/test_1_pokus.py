import pymysql
import pytest
from Projekt_2.Task_manager_SQL import add_task_overenie_input, add_task_into_sql, get_task_id, kontrola_id_status, update_task_status

#----ZADANIE: Testy ověří správnou funkčnost operací přidání, aktualizace a odstranění úkolů pomocí pytest.

# idealne spustit cez: pytest -s -v

conn = pymysql.connect(
                host="mysql80.r4.websupport.sk",
                port=3314,
                user="EsPMMROq",
                password="79_|rBg[1F=`}cj|I%kc",
                database="Task_manager_SQL"            
            )


# --------- test pro PRIDANI UKOLU 1---------
# add_tast_input - netestujeme

# def test_add_task_overenie_input_positive():
#     result = add_task_overenie_input(nazev_ukolu="ukol pro input", popis_ukolu="overenie funkcnosti string vstupu")
#     if result is not None:
#         print("✅ Spravne overenie zadanych vstupov")
#     assert result, f"❌ Necakana chyba pri spravnom zadani nazvu a popisu" 


# def test_add_task_overenie_input_negative():
#     result = add_task_overenie_input(nazev_ukolu="ukol pro input", popis_ukolu="")
#     if result is None:
#         print("✅ Spravne overenie nevyplnenych vstupov")

#     assert result is None, f"❌ Zapisuje ukol aj pri prazdnom vstupe" 


# def test_add_task_positive(): 
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


# def test_add_task_negative():

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


# ------------- testy na AKTUALIZOVAT UKOL -------


# def test_get_task_id_positive():
#     cursor=conn.cursor()
#     cursor.execute(
#         "INSERT INTO Ukoly_test (nazev, popis) VALUES ('ukol pro get task id', 'vytvorenie ulohy, aby zoznam nikdy nebol prazdny');"
#         )
#     conn.commit()
        
#     # Získame ID posledne vloženého záznamu
#     nove_id = cursor.lastrowid  # ⬅️ Lepšie ako "SELECT * FROM Ukoly_test ORDER BY id DESC LIMIT 1;"
#     cursor.close()

#     if nove_id:
#         print(f"✅ nove_id vlozenej ulohy je: {nove_id}")

#     result = get_task_id(conn, nove_id)
#     assert result == nove_id, f"❌ Očakávané ID {nove_id}, ale vrátené: {result}"


# def test_get_task_id_negative():
#     neexistujuce_id = 999999

#     result = get_task_id(conn, neexistujuce_id)
#     assert result is None

# def test_get_task_id_2_negative():
#     cursor = conn.cursor(pymysql.cursors.DictCursor) #aby si vedel vybrat kluc
#     cursor.execute("SELECT id FROM Ukoly_test ORDER BY id DESC LIMIT 1;")
#     max_id = cursor.fetchone()
#     cursor.close()
     
#     if max_id:
#         vyber = max_id["id"]
#     else:
#         vyber = 0

#     up_max_id = vyber + 1000 #aby sme mali 100% istotu

#     result = get_task_id(conn, up_max_id)
#     if result is None:
#         print(f"✅ Zadane id: {up_max_id} neexistuje podla ocakavania")

#     assert result is None, f"❌ Očakávané 'None' pre ID {max_id}, ale vrátené: {result}"


# def test_kontrola_id_status_positive(): #funkcia v kode vracia True ak sa nachazda v tabulke a  false ak nenajde take id

#     cursor=conn.cursor()
#     cursor.execute(
#         "INSERT INTO Ukoly_test (nazev, popis) VALUES ('ukol pre kontrolu id statusu', 'vytvorenie ulohy, aby sme zistili jej id, a aby zoznam nidy nebol prazdny');"
#         )
#     conn.commit()
        
#     nove_id = cursor.lastrowid  
#     cursor.close()

#     result = kontrola_id_status(conn, nove_id)

#     assert result is True, f"❌ Očakávané True pre existujúce ID {nove_id}, vrátené: {result}"

# def test_kontrola_id_status_negative():
#     neexistujuce_id= -1
#     result = kontrola_id_status(conn, neexistujuce_id)

#     assert result is False, f"❌ Očakávané False pre zaporne ID, vrátené: {result}"


# def test_update_task_status_get_id_positive():
#     zadanie_stavu = "Probíhá"

#     cursor=conn.cursor()
#     cursor.execute(
#         "INSERT INTO Ukoly_test (nazev, popis) VALUES ('ukol pre kontrolu update ulohy', 'vytvorenie ulohy, aby sme zistili jej id, a ci ju funkcia vyhodnoti spravne podla ocakavania');"
#         )
#     conn.commit()
        
#     nove_id = cursor.lastrowid  

#     result = update_task_status (conn, nove_id, zadanie_stavu)
    
#     assert result is True, f"❌ Očakávané True, zadali sme povoleny stav, hlasi {result}"

   
# def test_update_task_status_get_id_positive():
#     zadanie_stavu = "Hotovo"

#     cursor=conn.cursor()
#     cursor.execute(
#         "INSERT INTO Ukoly_test (nazev, popis) VALUES ('ukol pre kontrolu id statusu', 'vytvorenie ulohy, aby sme zistili jej id, pre aktualizaciu stavu');"
#         )
#     conn.commit()
        
#     nove_id = cursor.lastrowid

#     cursor.execute(
#         "SELECT id, nazev, stav FROM Ukoly_test WHERE id=%s;",
#         (nove_id,)
#     )
#     novy_ukol = cursor.fetchone()
#     cursor.close()

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


def test_update_task_status_get_id_negative():
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
        
    
    # assert sa nepouzije, lebo funkcia nema co vratit, vyhodi vynimnku



# # ------------- test na ZOBRAZIT UKOLY -------
# def test_get_all_tasks_positive(): #tu v zatvorke nesmie byt conn, lebo to berie ako fixture
#     cursor=conn.cursor()
#     cursor.execute(
#         "INSERT INTO Ukoly_test (nazev, popis) VALUES ('ukol pro seznam', 'vytvoreni ukol aby seznam nebyl nikdy prazdny');"
#         )
#     conn.commit()

#     tasks = get_all_tasks(conn)
#     if tasks is not None:
#         print("✅ Tabulka zobrazuje ulohy")

#     assert len(tasks) > 0  # očakávame, že sú tam nejaké tasky
#     assert "id" in tasks[0]
#     assert "nazev" in tasks[0]
#     assert tasks is not None, f"❌ ocekavany zaznam v tabulke, v skutocnosti zoznam prazdny"


# def test_get_all_tasks_negative():
#     #vycistime tabulku, aby sme zistili, ci reaguje na prazdny zoznam
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM Ukoly_test;")
#     conn.commit()
#     cursor.close()

#     tasks = get_all_tasks(conn)
#     if tasks is None:
#         print("✅ Zoznam je prazdny podla ocakavania")

#     assert tasks is None
    
# #poznamky pre mna: fetchall vracia vzdy list [], nie tuple() -> [{"id": 1, "nazev": "..."}]