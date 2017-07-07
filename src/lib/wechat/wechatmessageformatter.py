import time
import xmltodict

class WeChatMessageFormatter(object):
    # Check if the message XML is valid, this simple bot handles TEXT messages only!
    # To learn more about the supported types of messages and how to implement them, see:
    # Common Messages: http://admin.wechat.com/wiki/index.php?title=Common_Messages
    # Event Messages: http://admin.wechat.com/wiki/index.php?title=Event-based_Messages
    # Speech Recognition Messages: http://admin.wechat.com/wiki/index.php?title=Speech_Recognition_Messages
    def validate_incoming_message(self, message):
        return (
            message != None and
            message['xml'] != None and
            message['xml']['MsgType'] != None and
            message['xml']['MsgType'] == 'text' and
            message['xml']['Content'] != None
        )

    # Parse the native WeChat message XML format to a common format
    def parse_incoming_message(self, message):
        parsed_message = xmltodict.parse(message)
        if self.validate_incoming_message(parsed_message):
            return {
                'sender': parsed_message['xml']['FromUserName'],
                'receiver': parsed_message['xml']['ToUserName'],
                'type': parsed_message['xml']['MsgType'],
                'content': parsed_message['xml']['Content'],
                'valid': True
            }
        return { 'valid': False }

    # Format the reply according to the WeChat XML format for synchronous replies,
    # see: http://admin.wechat.com/wiki/index.php?title=Callback_Messages
    def format_instant_reply(self, incoming_message, response_content):
        return (
            "<xml>"
            "<ToUserName><![CDATA[%s]]></ToUserName>"
            "<FromUserName><![CDATA[%s]]></FromUserName>"
            "<CreateTime>%s</CreateTime>"
            "<MsgType><![CDATA[text]]></MsgType>"
            "<Content><![CDATA[%s]]></Content>"
            "</xml>"
        ) % (
            incoming_message['sender'], # From and To must be inverted in replies ;)
            incoming_message['receiver'], # Same as above!
            time.gmtime(),
            response_content
        )

    # Format the reply according to the WeChat JSON format for asynchronous replies,
    # see: http://admin.wechat.com/wiki/index.php?title=Customer_Service_Messages#Text_Message
    def format_delayed_reply(self, queued_message, response_content):
        return {
                'touser': queued_message['sender'],
                'msgtype': 'text',
                'text': {
                    'content': response_content
                }
            }
