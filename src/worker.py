import os
import logging

from dotenv import load_dotenv, find_dotenv
from lib.db.redismanager import RedisManager
from lib.wechat.wechatqueueprocessor import WeChatQueueProcessor

# Setup logger
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

# Load .env files for local development (DO NOT push it to production!)
load_dotenv(find_dotenv())

# Create a DatabaseManager instance
db_manager = RedisManager(os.getenv('REDIS_URL', ''))

# Get a queued message
queued_message = db_manager.get_queued_message()

# Process the queued message
if queued_message != None:
    queue_processor = WeChatQueueProcessor(os.getenv('WECHAT_APPID', ''), os.getenv('WECHAT_APPSECRET', ''))
    queue_processor.process_message(queued_message)
