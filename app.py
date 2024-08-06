import sqlite3

from flask import Flask, g

app = Flask(__name__)
DATABASE = 'expenses.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    return 'Welcome to the Expense Tracker!'

if __name__ == '__main__':
    app.run(debug=True)
    