from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt_identity, jwt_required,
                                set_access_cookies, set_refresh_cookies)
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
        refresh_token = create_refresh_token(identity={'username': user[1], 'email': user[2]})
        
        response = make_response(jsonify({'message': 'Login successful', 'user': {'username': user[1], 'email': user[2]}}))
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)
        
        response.set_cookie('access_token', access_token, httponly=True, secure=False, samesite='Lax')
        response.set_cookie('refresh_token', refresh_token, httponly=True, secure=False, samesite='Lax')
        
        return response
    return jsonify({'message': 'Invalid credentials'}), 401

@auth.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    try:
        csrf_token = request.headers.get('X-CSRF-Token')
        print(f"CSRF Token received: {csrf_token}")  # Debugging line

        identity = get_jwt_identity()
        print(f"Identity from refresh token: {identity}")  # Debugging line

        if not identity:
            print("No identity found in the refresh token.")  # Debugging line
            return jsonify({"msg": "Invalid refresh token"}), 401

        new_access_token = create_access_token(identity=identity)
        response = make_response(jsonify({'access_token': new_access_token}))
        set_access_cookies(response, new_access_token)
        return response
    except Exception as e:
        print(f"Error in refresh token handling: {str(e)}")  # Debugging line
        return jsonify({"msg": "Token refresh failed"}), 401


@auth.route('/logout', methods=['POST'])
def logout():
    response = make_response(jsonify({'message': 'Logout successful'}))
    response.set_cookie('access_token', '', expires=0, httponly=True, secure=False, samesite='Lax')
    response.delete_cookie('access_token')
    return response
