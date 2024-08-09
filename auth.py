from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash

from database import get_db

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO user (username, email, password_hash) VALUES (?, ?, ?)',
                   (data['username'], data['email'], hashed_password))
    db.commit()
    return jsonify({'message': 'User registered successfully!'})

@auth.route('/login', methods=['POST'])
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
