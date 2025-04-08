import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the environment variable

MYSQL_CONFIG = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "database": os.getenv("DB_NAME"),
}

MONGO_URI = os.getenv("MONGO_URI")
