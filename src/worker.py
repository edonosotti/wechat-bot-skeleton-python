import os

from dotenv import load_dotenv, find_dotenv
from lib.db.redismanager import RedisManager

# Load .env files for local development (DO NOT push it to production!)
load_dotenv(find_dotenv())

# Create a DatabaseManager instance
db_manager = RedisManager(os.getenv('REDIS_URL', ''))

