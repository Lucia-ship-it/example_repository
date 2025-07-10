def vytvoreni_tabulky(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Ukoly (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nazev VARCHAR (50) NOT NULL,
            popis VARCHAR (255) NOT NULL,
            stav  ENUM ('Nezahájeno', 'Probíhá', 'Hotovo') NOT NULL DEFAULT 'Nezahájeno', 
            datum_vytvoreni DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        print("✅ Tabulka 'Ukoly' je vytvořena.")
        conn.commit()
    except pymysql.MySQLError as err:
        print(f"Chyba při vytváření tabulky: {err}")
    finally:
        cursor.close()

Tvoje funkce vytvoreni_tabulky(conn) pracuje přímo s databází, takže pro její testování pomocí pytest budeme chtít:

✅ Otestovat:
že se zavolá SQL příkaz CREATE TABLE,

že se spustí commit(),

že se volá cursor.close() i v případě chyby.