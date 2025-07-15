import pymysql

conn = pymysql.connect(
                host="mysql80.r4.websupport.sk",
                port=3314,
                user="EsPMMROq",
                password="79_|rBg[1F=`}cj|I%kc",
                database="Task_manager_SQL"            
            )

cursor = conn.cursor()

if conn:
    print("\nPřipojení k databázi bylo úspěšné. Databáze Task_manager_SQL je k dispozici.")
