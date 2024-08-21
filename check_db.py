# check_db.py
import sqlite3

def check_tables():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM sqlite_master WHERE type="table";')
    tables = cursor.fetchall()
    conn.close()
    return tables

if __name__ == "__main__":
    tables = check_tables()
    print(tables)
