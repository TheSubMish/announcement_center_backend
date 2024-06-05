from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

class MongoDB:
    _connection_string = ""
    
    def __init__(self):
        self._connection_string =os.environ.get("MONGODB_CONNECTION_STRING")

    def connect_db(self, db_name):
        return MongoClient(self._connection_string,uuidRepresentation='standard')[db_name]

database = MongoDB()