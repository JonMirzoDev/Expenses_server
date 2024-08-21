from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from database import get_db

categories = Blueprint('categories', __name__)

@categories.route('/categories', methods=['POST'])
@jwt_required()
def add_category():
    data = request.get_json()
    current_user = get_jwt_identity()
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO category (name) VALUES (?)', (data['name'],))
    db.commit()
    return jsonify({'message': 'Category added successfully!'})


@categories.route('/categories', methods=['GET'])
@jwt_required()
def get_categories():
    db = get_db()
    cursor = db.cursor()

    # Get pagination parameters
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    offset = (page - 1) * per_page

    # Query to fetch total count of categories
    cursor.execute('SELECT COUNT(*) FROM category')
    total_categories = cursor.fetchone()[0]

    # Query to fetch categories with pagination
    cursor.execute(
        'SELECT * FROM category ORDER BY id DESC LIMIT ? OFFSET ?',
        (per_page, offset)
    )
    categories = cursor.fetchall()

    category_list = [{'id': category[0], 'name': category[1]} for category in categories]

    return jsonify({
        'categories': category_list,
        'total': total_categories
    })

@categories.route('/categories/<int:id>', methods=['PUT'])
@jwt_required()
def update_category(id):
    data = request.get_json()
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM category WHERE id = ?', (id,))
    category = cursor.fetchone()
    if not category:
        return jsonify({'message': 'Category not found'}), 404
    cursor.execute('UPDATE category SET name = ? WHERE id = ?', (data['name'], id))
    db.commit()
    return jsonify({'message': 'Category updated successfully!'})

@categories.route('/categories/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_category(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM category WHERE id = ?', (id,))
    category = cursor.fetchone()
    if not category:
        return jsonify({'message': 'Category not found'}), 404
    cursor.execute('DELETE FROM category WHERE id = ?', (id,))
    db.commit()
    return jsonify({'message': 'Category deleted successfully!'})