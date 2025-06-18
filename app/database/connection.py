from flask import Flask
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from loguru import logger
import os

db_logger = logger.bind(name="DB_CONNECTION")

def init_db(app: Flask) -> MongoClient:
    """
    Builds the client to use MongoDB

    Args:
        app (Flask): App (Flask) created previously
    Raises:
        ValueError: If the app (Flask) is missing
        ValueError: If the connection type is not finded
        ValueError: If the user or password is not finded in cloud connection
        ConnectionFailure: When the connection can't be done

    Returns:
        MongoClient: Client to use MongoDB
    """
    if app is None:
        raise ValueError("Missing app (Flask)")
    
    load_dotenv()
    
    try:
        USER: str | None = os.environ.get("DB_USER")
        PASSWORD: str | None = os.environ.get("DB_PASSWORD")
        CONNECTION: str | None = os.environ.get("DB_CONNECTION")
        
        if not CONNECTION:
            raise ValueError("DB_CONNECTION environment value required")
        
        if CONNECTION == "cloud" and (not USER or not PASSWORD):
            raise ValueError("DB_USER and DB_PASSWORD are required for cloud connection")
        
        
    except Exception as e:
        db_logger.error(f"Error loading environment variables: {e}")
        raise
    
    URI = _build_connection_uri(CONNECTION, USER, PASSWORD)
    
    try:
        MONGO_CLIENT = MongoClient(
            URI,
            serverSelectionTimeoutMS=5000, # 5 seconds timeout to select a server
            connectTimeoutMS=5000, # 5 seconds timeout to make a connection to the server
            maxPoolSize=5, # Max connections to the server
            retryWrites=True # Automatically retries writing actions
        )
        
        _test_connection(MONGO_CLIENT)
        
        app.config["MONGO_CLIENT"] = MONGO_CLIENT
        
        db_logger.success(f"Successfully connected to MongoDB ({CONNECTION} mode)")
        return MONGO_CLIENT

    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        db_logger.error(f"Failed to connect to MongoDB: {e}")
        raise ConnectionFailure(f"Cannot connect to MongoDB database: {e}")
    except Exception as e:
        db_logger.error(f"Unexpected error during database initialization: {e}")
        raise
    
def _build_connection_uri(connection_type: str, user: str | None = None, password: str | None = None) -> str:
    """
    Builds the connection URI based on the connection type

    Args:
        connection_type (str): Type of connection ('local' or 'cloud')
        user (str, optional): User for cloud connection. Defaults to None.
        password (str, optional): Password for cloud connection. Defaults to None.

    Raises:
        ValueError: If not User or Password in cloud connection type
        ValueError: If the connection type is invalid

    Returns:
        str: Connection URI
    """
    match connection_type.lower():
        case "local":
            return "mongodb://localhost:27017/"
        case "cloud":
            if not user or not password:
                raise ValueError("User and password required for cloud connection")
            return f"mongodb+srv://{user}:{password}@cleanlyfe.1ucxqaz.mongodb.net/?retryWrites=true&w=majority&appName=cleanlyfe"
        case _:
            raise ValueError(f"Invalid database connection type: {connection_type}. Use 'local' or 'cloud'")
        
def _test_connection(client: MongoClient) -> None:
    """
    Test connection to MongoDB
    
    Args:
        client (MongoClient): MongoDB client
        
    Raises:
        ConnectionFailure: If the connection fails
    """
    try:
        # Tries to ping the server
        client.admin.command('ping')
        db_logger.info("MongoDB connection test successful")
    except Exception as e:
        db_logger.error(f"MongoDB connection test failed: {e}")
        raise ConnectionFailure(f"Connection test failed: {e}")