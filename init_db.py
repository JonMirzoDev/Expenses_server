import sqlite3


def init_db():
    db = sqlite3.connect('expenses.db')
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            password_hash TEXT NOT NULL
        )               
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS category (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )               
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expense (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            description TEXT,
            date TEXT NOT NULL,
            category_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (category_id) REFERENCES category (id),
            FOREIGN KEY (user_id) REFERENCES user (id)
        )               
    ''')
    db.commit()
    db.close()
    
if __name__ == '__main__':
    init_db()