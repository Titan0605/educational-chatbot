from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from typing import Optional

mongo_client: Optional[MongoClient] = None

def save_db_for_utils(app_mongo: MongoClient) -> None:
    """Initialize the database connection"""
    global mongo_client
    mongo_client = app_mongo
    
def get_client() -> MongoClient:
    if mongo_client is None:
        raise RuntimeError("Database not initialized. Call init_db first.")
    
    return mongo_client
    
def get_db(database_name: str = "chatbot") -> Database:
    """Get a specific database from MongoDB client"""
    client: MongoClient = get_client()
    return client[database_name]

def get_collection(collection_name: str, database_name: str = "chatbot") -> Collection:
    """Get a specific collection from MongoDB"""
    db: Database = get_db(database_name)
    return db[collection_name]