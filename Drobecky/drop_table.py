import pymysql

conn = pymysql.connect(
        host="mysql80.r4.websupport.sk",
        port=3314,
        user="EsPMMROq",
        password="79_|rBg[1F=`}cj|I%kc",
        database="Task_manager_SQL#"      
    )

cursor=conn.cursor()
# cursor.execute(
#     "DROP TABLE Ukoly_test;")
