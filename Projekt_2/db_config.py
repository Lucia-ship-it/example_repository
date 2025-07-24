import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT")),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSW"),
    "database": os.getenv("DB_NAME")
}

def create_connection():
    return pymysql.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"]
    )

def create_table_if_not_exist(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Ukoly_test (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nazev VARCHAR(50) NOT NULL,
            popis VARCHAR(255) NOT NULL,
            stav ENUM('Nezahájeno', 'Probíhá', 'Hotovo') NOT NULL DEFAULT 'Nezahájeno',
            datum_vytvoreni DATE DEFAULT (CURRENT_DATE)
        );
    """)
    conn.commit()
    cursor.close()