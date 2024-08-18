from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from database import get_db

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard():
    user_identity = get_jwt_identity()
    print(f'User Identity: {user_identity}')  # Add this line for debugging
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM data WHERE email = ?', (user_identity['email'],))
    user_data = cursor.fetchone()

    return jsonify({
        'message': 'Welcome to your dashboard!',
        'user_data': user_data
    })

