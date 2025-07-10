import pymysql
import pytest #instalacia: pip3 install -U pytest
#from Task_manager_SQL.py import vytvoreni_tabulky

#pytest prve_nacrty.py - spustenie, lebo dokument sa nevola test_...

def pripojenie():
    conn = pymysql.connect(
        host="mysql80.r4.websupport.sk",
        port=3314,
        user="EsPMMROq",
        password="79_|rBg[1F=`}cj|I%kc",
        database="Task_manager_SQL"            
    )
    print("\nPřipojení k databázi bylo úspěšné. Databáze Task_manager_SQL je k dispozici.")
    return conn

def pridani_ukolu_db(conn, nazev, popis):
    if nazev == "":
        return None
    if popis == "":
        return None
    cursor = conn. cursor()
    cursor.execute(
        "ÏNSERT INTO Ukoly_test (nazev, popis) VALUES (%s,%s);",
        (nazev, popis)
    )
    conn.commit()
    cursor.close()

# def pridani_ukolu():
#     while True: #osetrenie prazdneho vstupu
#         nazev = input("Zadejte název úkolu: ").strip()
#         if nazev != "":
#             return nazev
#         break
                
#     while True:
#        popis = input("Zadejte popis úkolu: ").strip()
#        if popis != "":
#             return popis
#        break
def pridani_ukolu(nazev: str, popis: str) -> str:
    nazev = nazev.strip()
    popis = popis.strip()
    if not nazev or not popis:
        return ""
    return f"{nazev}: {popis}"  
# Nevolá input(), ale prijíma nazev a popis ako argumenty, ktore zadam v teste

def test_pridani_ukolu():
    result = pridani_ukolu(nazev="Ukol 1", popis="Popis ukolu 1")
    assert result == "Ukol 1: Popis ukolu 1"

def test_pridani_ukolu_prazdny_nazev():
    result = pridani_ukolu(nazev=" ", popis="Popis")
    assert result == ""

def test_pridani_ukolu_prazdny_popis():
    result = pridani_ukolu(nazev="Nazev", popis=" ")
    assert result == ""
#test
# @pytest.mark.positive
# def test_pridani_ukolu()
#     result = pridani_ukolu(nazev='ukol 1', popis='popis ukolu 1')
#     assert result != ""

# def test_pocitanie():
#     result = 1+1
#     assert result == 2

# def test_pocitanfffie():
#     result = 1+1
#     assert result != 9