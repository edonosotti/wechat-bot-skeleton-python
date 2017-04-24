# Define an interface for possible future implementations of queue processors for other messenger platforms
class IQueueProcessor(object):
    def process_message(self, message):
        raise Exception('Not implemented')
