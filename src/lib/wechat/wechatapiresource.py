import hashlib
import time
import falcon
import xmltodict

# Adapted from: https://gist.github.com/edonosotti/8c4a06eef3ecf80b320ecc2e09a520a9
# See: https://falcon.readthedocs.io/en/stable/user/quickstart.html
class WeChatApiResource(object):
    def __init__(self, db_manager, token):
        self.db_manager = db_manager
        self.token = token

    # Check if the message XML is valid, this simple bot handles TEXT messages only!
    # To learn more about the supported types of messages and how to implement them, see:
    # Common Messages: http://admin.wechat.com/wiki/index.php?title=Common_Messages
    # Event Messages: http://admin.wechat.com/wiki/index.php?title=Event-based_Messages
    # Speech Recognition Messages: http://admin.wechat.com/wiki/index.php?title=Speech_Recognition_Messages
    def validate_message(self, message):
        return (
            message != None and
            message['xml'] != None and
            message['xml']['MsgType'] != None and
            message['xml']['MsgType'] == 'text' and
            message['xml']['Content'] != None
        )

    # Format the reply according to the WeChat XML format for synchronous replies,
    # see: http://admin.wechat.com/wiki/index.php?title=Callback_Messages
    def format_message(self, original_message, content):
        return (
            "<xml>"
            "<ToUserName><![CDATA[%s]]></ToUserName>"
            "<FromUserName><![CDATA[%s]]></FromUserName>"
            "<CreateTime>%s</CreateTime>"
            "<MsgType><![CDATA[text]]></MsgType>"
            "<Content><![CDATA[%s]]></Content>"
            "</xml>"
        ) % (
            original_message['xml']['FromUserName'], # From and To must be inverted in replies ;)
            original_message['xml']['ToUserName'], # Same as above!
            time.gmtime(),
            content
        )

    # The WeChat server will issue a GET request in order to verify the chatbot backend server upon configuration.
    # See: http://admin.wechat.com/wiki/index.php?title=Getting_Started#Step_2._Verify_validity_of_the_URL
    # and: http://admin.wechat.com/wiki/index.php?title=Message_Authentication
    def on_get(self, request, response):
        # Get the parameters from the query string
        signature = request.get_param('signature')
        timestamp = request.get_param('timestamp')
        nonce = request.get_param('nonce')
        echostr = request.get_param('echostr')

        # Compute the signature (note that the shared token is used too)
        verification_elements = [self.token, timestamp, nonce]
        verification_elements.sort()
        verification_string = "".join(verification_elements)
        verification_string = hashlib.sha1(verification_string.encode('utf-8')).hexdigest()

        # If the signature is correct, output the same "echostr" provided by the WeChat server as a parameter
        if signature == verification_string:
          response.status = falcon.HTTP_200
          response.body = echostr
        else:
          response.status = falcon.HTTP_500
          response.body = ""

    # Messages will be POSTed from the WeChat server to the chatbot backend server,
    # see: http://admin.wechat.com/wiki/index.php?title=Common_Messages
    def on_post(self, request, response):
        # Parse the WeChat message XML format
        message = xmltodict.parse(request.bounded_stream.read())

        if self.validate_message(message):
            # WeChat always requires incoming user messages to be acknowledged at
            # least with an empty string (empty strings are not shown to users),
            # see: https://chatbotsmagazine.com/building-chatbots-for-wechat-part-1-dba8f160349
            # In this sample app, we simulate a "Customer Service"-like scenario
            # providing an instant reply to the user, announcing that a complete
            # reply will follow.
            self.db_manager.queue_message(message)
            reply = "Thank you for your message. We will get back to you as soon as possible!"
            response.status = falcon.HTTP_200
            response.body = self.format_message(message, reply)
        else:
            response.status = falcon.HTTP_200
            response.body = "Message was sent in a wrong format."
