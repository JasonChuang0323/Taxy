# Taxy


## Running the Application

To start the application, use the following command:

```sh
python run.py

This will launch the server on http://127.0.0.1:5000.

Access the Home Page
To make a GET request to the root URL, use:

curl http://127.0.0.1:5000/

sample register request

curl -X POST http://localhost:5000/register -H "Content-Type: application/json" -d '{"username": "jas", "password": "1223"}'


Dependencies

Ensure you have the required dependencies installed. If you are using requirements.txt, you can install them with:

pip install -r requirements.txt


###Setup MongoDb locally

brew tap mongodb/brew

brew install mongodb-community

brew services start mongodb-community

mongosh

if you want to disconnect the db:
brew services stop mongodb-community

