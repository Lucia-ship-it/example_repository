from ukoly_input import add_task_input
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
    add_task_input(conn)
    conn.close()