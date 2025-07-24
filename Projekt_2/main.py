import importlib
from dotenv import load_dotenv
import os

load_dotenv()
library = os.getenv("LIBRARY")
if library == "pymysql":
    db = importlib.import_module("Projekt_2.Task_manager_TEST_SQL")


if __name__ == "__main__":
    passwd = os.getenv("DB_PASSW")

    conn = db.connect_to_db("mysql80.r4.websupport.sk",3314, "luciakobzova", passwd, "luciakobzova")
    db.close_connection(conn)