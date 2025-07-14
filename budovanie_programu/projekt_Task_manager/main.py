from ukoly_input import add_task_input
from ukoly_sql import create_table_if_not_exist
import pymysql

#spúšťací súbor (napr. menu, výber akcií)

def vytvor_pripojeni(): #slo by na test
    try:
        conn = pymysql.connect(
                host="mysql80.r4.websupport.sk",
                port=3314,
                user="EsPMMROq",
                password="79_|rBg[1F=`}cj|I%kc",
                database="Task_manager_SQL"            
            )
        print("\nPřipojení k databázi bylo úspěšné. Databáze Task_manager_SQL je k dispozici.")
        
        return conn
    except pymysql.MySQLError as err:
        print(f"❌ Chyba při připojování: {err}")   
        return None        
        
if __name__ == "__main__":
    conn = vytvor_pripojeni()
    if conn:
        if create_table_if_not_exist(conn):
            print("✅ Tabulka je připravená.")
        else:
            print("❌ Chyba při přípravě tabulky.")
    else:
        print("❌ Nepodařilo se připojit k databázi.")
   
    conn.close()