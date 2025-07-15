import pymysql

def vytvor_pripojeni(): 
    try:
        conn = pymysql.connect(
                host="mysql80.r4.websupport.sk",
                port=3314,
                user="EsPMMROq",
                password="79_|rBg[1F=`}cj|I%kc",
                database="Task_manager_SQL"            
            )
        print("\n✅ Připojení k databázi bylo úspěšné. Databáze Task_manager_SQL je k dispozici.")
        
        return conn
    except pymysql.MySQLError as err:
        print(f"❌ Chyba při připojování: {err}")   
        return None 
    

    #testy
# test_pripojeni.py

# from pripojeni import vytvor_pripojeni

#pozitivny test
# def test_vytvor_pripojeni():
#     conn = vytvor_pripojeni()
#     assert conn is not None  # ✅ Test prejde len ak sa podarí pripojenie

#     # Extra overenie: objekt má metódu cursor()
#     assert hasattr(conn, 'cursor')

#     conn.close()

#aby sme spravili negativny test, musime upravit definiciu
# import pymysql

# def vytvor_pripojeni_custom(host, user, password, database, port=3306):
#     try:
#         conn = pymysql.connect(
#             host=host,
#             port=port,
#             user=user,
#             password=password,
#             database=database
#         )
#         return conn
#     except pymysql.MySQLError:
#         return None

# from pripojeni import vytvor_pripojeni_custom

# def test_vytvor_pripojeni_negativni():
#     conn = vytvor_pripojeni_custom(
#         host="localhost",
#         user="root",
#         password="zle_heslo",  # úmyselne nesprávne
#         database="ukoly_test"
#     )
#     assert conn is None  # očakávame, že sa pripojenie NEpodarí

# Áno, máš úplnú pravdu – ak potrebuješ pripojenie takmer vo všetkých funkciách (napr. na vkladanie, aktualizáciu, výpis, atď.), je veľmi praktické mať samostatnú funkciu na pripojenie k databáze, ktorú voláš na začiatku (napr. v main.py) a potom ju odovzdávaš ako parameter ďalej.