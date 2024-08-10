from flask import Blueprint, jsonify, request

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