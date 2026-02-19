from motor.motor_asyncio import AsyncIOMotorClient
from src.config import CONFIG

mongo_client = None
database = None


def connect_mongo():
    global mongo_client, database
    mongo_client = AsyncIOMotorClient(CONFIG.MONGO_URI)
    database = mongo_client[CONFIG.MONGO_DB_NAME]

    print("Connected to DB")

def get_db():
    return database
