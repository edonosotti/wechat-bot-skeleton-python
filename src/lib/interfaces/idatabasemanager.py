# Define an interface for possible future implementations of database managers.
class IDatabaseManager:
    def __init__(self, database_url):
        raise Exception('Not implemented')

    def queue_message(self, message):
        raise Exception('Not implemented')

    def get_queued_message(self):
        raise Exception('Not implemented')
