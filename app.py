from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from auth import auth as auth_blueprint
from categories import categories as categories_blueprint
from dashboard import dashboard as dashboard_blueprint
from database import close_connection, get_db
from expenses import expenses as expenses_blueprint

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=['http://localhost:3000'])
app.config['JWT_SECRET_KEY'] = 'your_secret_key'
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
jwt = JWTManager(app)

app.teardown_appcontext(close_connection)

# Register blueprints
app.register_blueprint(auth_blueprint)
app.register_blueprint(expenses_blueprint)
app.register_blueprint(categories_blueprint)
app.register_blueprint(dashboard_blueprint)

@app.route('/')
def home():
    return "Welcome to the Expense Tracker!"

if __name__ == '__main__':
    app.run(debug=True)
