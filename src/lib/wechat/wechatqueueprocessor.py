import json
import logging
import urllib.request

from ..interfaces.iqueueprocessor import IQueueProcessor

class WeChatQueueProcessor(IQueueProcessor):
    WECHAT_URL = "https://api.wechat.com/cgi-bin"

    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret

    # See: http://admin.wechat.com/wiki/index.php?title=Access_token
    def get_access_token(self):
        url = (
            "%s/token"
            "?grant_type=client_credential"
            "&appid=%s"
            "&secret=%s"
        ) % (
            self.WECHAT_URL,
            self.app_id,
            self.app_secret
        )

        response = urllib.request.urlopen(url)
        response_body = response.read().decode('utf-8')
        token_info = json.loads(response_body)

        if not 'errcode' in token_info:
            return token_info['access_token']

        logging.error("Error getting WeChat access token: %s", response_body)
        return None

    # See: http://admin.wechat.com/wiki/index.php?title=Customer_Service_Messages
    def process_message(self, message):
        access_token = self.get_access_token()

        if access_token != None:
            url = "%s/message/custom/send?access_token=%s" % (self.WECHAT_URL, access_token)
            request_body = {
                'touser': message['sender'],
                'msgtype': 'text',
                'text': {
                    'content': 'Your request has been processed, thank you!'
                }
            }

            response = urllib.request.urlopen(url, json.dumps(request_body).encode('utf-8'))
            response_body = response.read().decode('utf-8')
            result = json.loads(response_body)

            if 'errcode' in result and result['errcode'] == 0:
                return True
            else:
                logging.error("Error sending Customer Service type message: %s", response_body)

        return False
