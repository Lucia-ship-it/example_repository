#obsahuje databázové funkcie (SQL)

def add_task_into_sql(conn,nazev_ukolu, popis_ukolu):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Ukoly_test (nazev, popis) VALUES (%s,%s);", 
        (nazev_ukolu.strip(), popis_ukolu.strip())
        )
    conn.commit()
    cursor.close()