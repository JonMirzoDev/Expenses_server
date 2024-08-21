import os
import sqlite3

from flask import g

DATABASE = os.getenv('DATABASE_URL', 'sqlite:///expenses.db')  # Get DATABASE_URL from environment

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
