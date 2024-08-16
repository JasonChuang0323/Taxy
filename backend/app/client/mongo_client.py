from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, PyMongoError

class MongoDBClient:
    def __init__(self, uri='mongodb://localhost:27017/', db_name='Taxy'):
        self.client = None
        self.db = None
        self.uri = uri
        self.db_name = db_name
        self.connect()

    def connect(self):
        try:
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=5000)
            # Attempt to get a server response to confirm the connection is established
            self.client.server_info()
            self.db = self.client[self.db_name]
            print("Connected to MongoDB")
        except ServerSelectionTimeoutError:
            print("Could not connect to MongoDB: Server selection timeout")
        except PyMongoError as e:
            print(f"Could not connect to MongoDB: {e}")

    def get_collection(self, collection_name):
        if self.db is None:
            raise RuntimeError("Not connected to MongoDB")
        return self.db[collection_name]
    
    def close(self):
        if self.client:
            self.client.close()
            print("MongoDB connection closed")
