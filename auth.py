from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import create_access_token, jwt_required
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
        response = make_response(jsonify({'message': 'Login successfull', 'user': {'username': user[1], 'email': user[2]}}))
        response.set_cookie('access_token', access_token, httponly=True, secure=True, samesite='Lax')
        return response
    return jsonify({'message': 'Invalid credentials'}), 401

@auth.route('/logout', methods=['POST'])
def logout():
    response = make_response(jsonify({'message': 'Logout successful'}))
    response.set_cookie('access_token', '', expires=0, httponly=True, secure=True, samesite='Lax')
    return response
