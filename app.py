import logging
import os
from datetime import timedelta
from init_db import init_db

from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from auth import auth as auth_blueprint
from categories import categories as categories_blueprint
from dashboard import dashboard as dashboard_blueprint
from database import close_connection, get_db
from expenses import expenses as expenses_blueprint

load_dotenv()

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=['http://localhost:3000'])

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
app.config['JWT_COOKIE_SECURE'] = True
app.config['JWT_COOKIE_SAMESITE'] = 'None'
app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
app.config['JWT_REFRESH_COOKIE_PATH'] = '/token/refresh'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=10)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=7) 
jwt = JWTManager(app)

app.teardown_appcontext(close_connection)

# Register blueprints
app.register_blueprint(auth_blueprint)
app.register_blueprint(expenses_blueprint)
app.register_blueprint(categories_blueprint)
app.register_blueprint(dashboard_blueprint)

@app.before_request
def log_request_info():
    logging.info(f"Headers: {request.headers}")
    logging.info(f"Cookies: {request.cookies}")
    logging.info(f"CSRF Token Header: {request.headers.get('X-CSRF-Token')}")

@app.route('/')
def home():
    return "Welcome to the Expense Tracker!"

if __name__ == '__main__':
    if not os.path.exists('expenses.db'):
        print("Database not found. Initializing...")
        init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

