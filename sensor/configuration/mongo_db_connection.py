
import pymongo
from sensor.constants.database import DATABASE_NAME
from sensor.constants.env_variables import MONGODB_URL_KEY
import certifi , os
from dotenv import load_dotenv


ca = certifi.where()

class MongoDBClient:
    client = None
    def __init__(self,database_name = DATABASE_NAME)->None:
        try:
            if MongoDBClient.client is None:
                load_dotenv()
                MongoDBClient.client = pymongo.MongoClient(MONGODB_URL_KEY, tlsCAFile = ca)
            self.client = MongoDBClient.client
            self.database = self.client[database_name]  
            self.database_name = database_name
        except Exception as e:
            raise e              