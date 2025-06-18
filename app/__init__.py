from flask import Flask
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import logging
from app.database.connection import init_db

logger = logging.getLogger(__name__)

def app_init() -> Flask:
    app = Flask(__name__)
    
    try:
        mongo_client: MongoClient = init_db(app)
    except (ConnectionFailure, ValueError) as e:
        logger.error(f"Failed to initialize database: {e}")
        raise
    
    return app