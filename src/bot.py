import os
import falcon
import logging

from dotenv import load_dotenv, find_dotenv
from .lib.db.redismanager import RedisManager
from .lib.wechat.wechatapiresource import WeChatApiResource

# Setup logger
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

# Load .env files for local development (DO NOT push it to production!)
load_dotenv(find_dotenv())

# Create a DatabaseManager instance
db_manager = RedisManager(os.getenv('REDIS_URL', ''))

# Init Falcon
api = application = falcon.API()

# Map a route (see: https://falcon.readthedocs.io/en/stable/api/api.html#falcon.API.add_route)
api.add_route('/wechat', WeChatApiResource(db_manager, os.getenv('WECHAT_TOKEN', '')))
