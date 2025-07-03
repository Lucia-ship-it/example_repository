import pymysql

try:
    conn = pymysql.connect(
            host="mysql80.r4.websupport.sk",
            port=3314,
            user="EsPMMROq",
            password="79_|rBg[1F=`}cj|I%kc",
            database="Task_manager_SQL"            
        )
    print("Připojení k databázi bylo úspěšné.")
except pymysql.connect.Error as err:
     print(f"Chyba při připojování: {err}")

cursor = conn.cursor()

# try:
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS Produkty (
#         id INT PRIMARY KEY AUTO_INCREMENT,
#         name VARCHAR(200) NOT NULL,
#         price DECIMAL(10,2),
#         in_storage INT
#         )
#     ''')
#     print("Tabulka 'Produkty' byla vytvořena.")

# except pymysql.connector.Error as err:
#     print(f"Chyba při vytváření tabulky: {err}")
# print("Připojení k databázi bylo uzavřeno.")