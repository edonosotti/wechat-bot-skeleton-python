import pytest
import os

from lib.db.redismanager import RedisManager

def test_redismanager():
    # WARNING
    # The Queue Manager implements the FIFO pattern, so in order for tests to
    # succeed, they MUST be ran against a private Redis instance where no other
    # processes are running I/O operations.
    message = { 'name': 'test' }
    db = RedisManager(os.getenv('REDIS_URL', ''))
    db.queue_message(message)
    queued_message = db.get_queued_message()
    assert 'name' in queued_message
    assert queued_message['name'] == 'test'
