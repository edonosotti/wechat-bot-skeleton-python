import redis
import pickle

from .idatabasemanager import IDatabaseManager

class RedisManager(IDatabaseManager):
    KEY_MESSAGE_QUEUE = 'message_queue'

    def __init__(self, redis_url):
        self.connection = redis.Redis.from_url(redis_url)

    def queue_message(self, message):
        serialized_message = pickle.dumps(message)
        self.connection.rpush(self.KEY_MESSAGE_QUEUE, message)
        # self.connection.save()

    def get_queued_message(self):
        serialized_message = self.connection.lpop(self.KEY_MESSAGE_QUEUE)
        print(serialized_message)
        # self.connection.save()
        if serialized_message != None:
            return pickle.loads(serialized_message)
        return None
