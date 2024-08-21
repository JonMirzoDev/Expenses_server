from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from database import get_db

expenses = Blueprint('expenses', __name__)

# add expense
@expenses.route('/expenses', methods=['POST'])
@jwt_required()
def add_expense():
    data = request.get_json()
    current_user = get_jwt_identity()
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT id FROM user WHERE email = ?', (current_user['email'],))
    user_id = cursor.fetchone()[0]
    cursor.execute('INSERT INTO expense (amount, description, date, category_id, user_id) VALUES (?, ?, ?, ?, ?)',
                   (data['amount'], data['description'], data['date'], data['category_id'], user_id))
    db.commit()
    return jsonify({'message': 'Expense added successfully!'})

# get all expenses with pagination
@expenses.route('/expenses', methods=['GET'])
@jwt_required()
def get_expenses():
    current_user = get_jwt_identity()
    category_id = request.args.get('category_id')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    offset = (page - 1) * per_page

    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT id FROM user WHERE email = ?', (current_user['email'],))
    user_id = cursor.fetchone()[0]

    # Query to fetch expenses with optional filtering by category_id and pagination
    if category_id:
        cursor.execute(
            'SELECT * FROM expense WHERE user_id = ? AND category_id = ? ORDER BY id DESC LIMIT ? OFFSET ?',
            (user_id, category_id, per_page, offset)
        )
        total_cursor = db.execute(
            'SELECT COUNT(*) FROM expense WHERE user_id = ? AND category_id = ?',
            (user_id, category_id)
        )
    else:
        cursor.execute(
            'SELECT * FROM expense WHERE user_id = ? ORDER BY id DESC LIMIT ? OFFSET ?',
            (user_id, per_page, offset)
        )
        total_cursor = db.execute(
            'SELECT COUNT(*) FROM expense WHERE user_id = ?',
            (user_id,)
        )

    expenses = cursor.fetchall()
    total_expenses = total_cursor.fetchone()[0]

    expense_list = []
    for expense in expenses:
        expense_list.append({
            'id': expense[0],
            'amount': expense[1],
            'description': expense[2],
            'date': expense[3],
            'category_id': expense[4],
            'user_id': expense[5]
        })

    return jsonify({
        'expenses': expense_list,
        'total': total_expenses,
        'page': page,
        'per_page': per_page
    })


# update expense
@expenses.route('/expenses/<int:id>', methods=['PUT'])
@jwt_required()
def update_expense(id):
    data = request.get_json()
    current_user = get_jwt_identity()
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT id FROM user WHERE email = ?', (current_user['email'],))
    user_id = cursor.fetchone()[0]
    cursor.execute('SELECT * FROM expense WHERE id = ? AND user_id = ?', (id, user_id))
    expense = cursor.fetchone()
    if not expense:
        return jsonify({'message': 'Expense not found'}), 404
    cursor.execute('UPDATE expense SET amount = ?, description = ?, category_id = ? WHERE id = ? ', (data['amount'], data['description'], data['category_id'], id))
    db.commit()
    return jsonify({'message': 'Expense updated successfully'})

# delete expense
@expenses.route('/expenses/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_expense(id):
    current_user = get_jwt_identity()
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT id FROM user WHERE email = ?', (current_user['email'],))
    user_id = cursor.fetchone()[0]
    cursor.execute('SELECT * FROM expense WHERE id = ? AND user_id = ?', (id, user_id))
    expense = cursor.fetchone()
    if not expense:
        return jsonify({'message': 'Expense not found'}), 404
    cursor.execute('DELETE FROM expense WHERE id = ?', (id,))
    db.commit()
    return jsonify({'message': 'Expense deleted successfully!'})