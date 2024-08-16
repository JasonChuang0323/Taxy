import bcrypt
from app.model.user import UserModel

class UserService:
    def __init__(self, mongo_client):
        self.mongo_client = mongo_client
        self.collection = self.mongo_client.get_collection('users')

    def user_exists(self, username):
        return self.collection.find_one({'username': username}) is not None

    def create_user(self, username, password):
        if self.user_exists(username):
            return {'error': 'Username already exists'}, 409

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user_model = UserModel(username, hashed_password.decode('utf-8'))

        user_document = {
            'username': user_model.username,
            'password': user_model.password
        }
        result = self.collection.insert_one(user_document)
        return {'_id': str(result.inserted_id)}, 201
