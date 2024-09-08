from flask import Blueprint, jsonify, request
from app.client.mongo_client import MongoDBClient
from app.service.user_service import UserService
from app.service.exchange_rate_service import ExchangeRateService
from app.exception.user_exception import UserException
from app.constant import Exchange_RATE_FILE_PATH
import bcrypt
import traceback

# Create a Blueprint for the routes
routes_bp = Blueprint('routes', __name__)

# Initialize MongoDB client
mongo_client = MongoDBClient()
user_service = UserService(mongo_client)
exchange_rate_servie = ExchangeRateService(mongo_client, Exchange_RATE_FILE_PATH)

@routes_bp.route('/')
def home():
    return 'Hello, welcome!'


@routes_bp.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.json
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Invalid input, must include username and password'}), 400

        username = data['username']
        password = data['password']

        response, status_code = user_service.create_user(username, password)
        return jsonify(response), status_code

    except Exception as e:
        raise UserException('An error occurred while creating the user') from e


@routes_bp.route('/login', methods=['POST'])
def login():
    ## refactoring this to login repo
    try:
        data = request.json
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Invalid input, must include username and password'}), 400

        username = data['username']
        password = data['password']

        users_collection = mongo_client.get_collection('users')
        
        user = users_collection.find_one({'username': username})

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return jsonify({'message': 'Login successful'}), 200
        else:
            return jsonify({'error': 'Invalid username or password'}), 401

    except Exception as e:
        raise UserException('An error occurred during login') from e


@routes_bp.route('/initial_exchange_rate', methods=['GET'])
def initial_exchange_rate():
    try:
        df = exchange_rate_servie.export_stock_value_based_on_exchange()
        return jsonify({'message': 'Stock rate calculated and saved'}), 200
    except Exception as e:
        raise UserException('An error occurred during login') from e



