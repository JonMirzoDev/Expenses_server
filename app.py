import sqlite3

from flask import Flask, g, jsonify, request
from flask_jwt_extended import (JWTManager, create_access_token,
                                get_jwt_identity, jwt_required)
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_secret_key'
jwt = JWTManager(app)
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

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO user (username, email, password_hash) VALUES (?, ?, ?)',
                   (data['username'], data['email'], hashed_password))
    db.commit()
    return jsonify({'message': 'User registered successfully!'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM user WHERE email = ?', (data['email'],))
    user = cursor.fetchone()
    if user and check_password_hash(user[3], data['password']):
        access_token = create_access_token(identity={'username': user[1], 'email': user[2]})
        return jsonify(access_token=access_token)
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/')
def home():
    return "Welcome to the Expense Tracker!"

if __name__ == '__main__':
    app.run(debug=True)

    