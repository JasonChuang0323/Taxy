from flask import Blueprint, jsonify, request
from .constant import UserList

# Create a Blueprint for the routes
routes_bp = Blueprint('routes', __name__)


@routes_bp.route('/')
def home():
    return 'Hello, welcome!'

@routes_bp.route('/api/greet', methods=['POST'])
def greet():
    data = request.get_json()
    name = data.get('name', 'Stranger')
    return jsonify({'message': f'Hello, {name}!'})

@routes_bp.route('/api/list_user')
def list_user():
    user_list = list(user.to_dict() for user in UserList)
    return jsonify(user_list)
