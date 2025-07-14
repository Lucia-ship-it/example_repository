import pymysql
import pytest
from Projekt_2.Task_manager_SQL import add_task_into_sql, get_all_tasks

# idealne spustit cez: pytest -s -v

conn = pymysql.connect(
                host="mysql80.r4.websupport.sk",
                port=3314,
                user="EsPMMROq",
                password="79_|rBg[1F=`}cj|I%kc",
                database="Task_manager_SQL"            
            )
# 1. mozeme pridat ukol 1
# 2. get contact ukol 1
# 3. zmazat ukol 1

# --------- test pro PRIDANI UKOLU ---------
# def test_pridani_ukolu_poaitive(): 
    
#     add_task_into_sql(conn,nazev_ukolu="Ukol1", popis_ukolu="popis k Ukol1")
    
#     cursor = conn.cursor(pymysql.cursors.DictCursor)
#     cursor.execute(# overime, ci tam je
#         "SELECT id, nazev, popis FROM Ukoly_test WHERE nazev =%s;",
#         ("Ukol1",)
#     ) 
#     result = cursor.fetchone()
#     print(result)
#     cursor.close()

#     assert result["nazev"] == "Ukol1"
#     assert result["popis"] == "popis k Ukol1"
#     assert result is not None

#------treba upravit aby neukladal prazdny zoznam-----

# def test_pridani_ukolu_negative():

#     add_task_into_sql(conn,nazev_ukolu="Ukol 2", popis_ukolu="")
#     assert  "VallueError"
#     if nazev_ukolu == "":
#         return None
#     if popis_ukolu == "":
#         return None
#     assert result is None, f"ocekavano None, ve skutecnosti {result}"


    # cursor = conn.cursor(pymysql.cursors.DictCursor)
    # cursor.execute(
    #     "SELECT id, nazev, popis FROM Ukoly_test WHERE nazev =%s;",
    #     ("Ukol2",)
    # ) 
    # result = cursor.fetchone()
    # print("vyplneni pole pro nazev a popis jsou povinne")
    # cursor.close()

    
# ------------- test na ZOBRAZIT UKOLY -------

def test_get_all_tasks_positive(): #tu v zatvorke nesmie byt conn, lebo to berie ako fixture
    cursor=conn.cursor()
    cursor.execute(
        "INSERT INTO Ukoly_test (nazev, popis) VALUES ("ukol pro seznam", "vytvoreni ukol aby seznam nebyl nikdy prazdny");
        )
    conn.commit()
                   
    tasks = get_all_tasks(conn)

    assert len(tasks) > 0  # očakávame, že sú tam nejaké tasky
    assert "id" in tasks[0]
    assert "nazev" in tasks[0]


# def test_get_all_tasks_negative():
#     #vycistime tabulku, aby sme zistili, ci reaguje na prazdny zoznam
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM Ukoly_test;")
#     conn.commit()
#     cursor.close()

#     tasks = get_all_tasks(conn)
#     assert tasks == () # tabulka vracia prazdny zoznam
