import sqlite3

DB_NAME = "../prototype/database.db"

def run_query(query):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(query)
    rows = c.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    print("Event Popularity:", run_query("SELECT * FROM events"))
