import sqlite3

from flask import g

DATABASE = 'expenses.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        # Connect to the database using the URL
        db = g._database = sqlite3.connect(DATABASE.split(':///')[-1])
    return db

def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
