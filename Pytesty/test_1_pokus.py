import pymysql
import pytest
from Projekt_2 import Task_manager_SQL


# 1. mozeme pridat ukol 1
# 2. get contact ukol 1
# 3. zmazat ukol 1

contacts = [{"name":"Luc", "phone":"8888888"},{"name":"Mat","phone":"77777"}]
def get_contact(name:str):
    for contact in contacts:
        if contacts["name"] == name:
            return(contact)
#pokud cyklus dobehol a nic nevratil, nech vrati None
    return None

# vyzada si kontakt
# pokud existuje, tak ho vytiskne
# ak neexistuje, hodi neexistuje

def test_pridani_ukolu_pozitivni():
    nazev_ukolu = input("zadej nazev ukolu: ") #zadej: Ukol1
    popis_ukolu= input("zadej popis ukolu: ") #zadej: popis k Ukol1

    result = add_task_into_sql(conn,nazev_ukolu, popis_ukolu)

    if result:
        print(result)
    else:
        print("dany ukol neulozen")

def test_pridani_ukolu_negativni_test():
    nazev_ukolu = input("zadej nazev ukolu: ") #zadej: Ukol1
    popis_ukolu= input("zadej popis ukolu: ") #zadej: 

    result = add_task_into_sql(conn,nazev_ukolu, popis_ukolu)

    if result is None:
        print("spravne neulozeno")
    else:
        print("jina chyba")
