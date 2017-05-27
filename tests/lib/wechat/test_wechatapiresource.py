import pytest
import falcon
import time
import hashlib
import xmltodict

from falcon import testing
from lib.interfaces.idatabasemanager import IDatabaseManager
from lib.wechat.wechatapiresource import WeChatApiResource

class DummyDatabaseManager(IDatabaseManager):
    def __init__(self, database_url):
        pass

    def queue_message(self, message):
        pass

    def get_queued_message(self):
        pass

@pytest.fixture()
def client():
    db_manager = DummyDatabaseManager('TEST_DATABASE_URL')
    application = falcon.API()
    application.add_route(
        '/wechat', WeChatApiResource(db_manager, 'TEST_WECHAT_TOKEN')
    )
    return testing.TestClient(application)

@pytest.fixture()
def message():
    return (
        "<xml>"
        "<ToUserName><![CDATA[toUser]]></ToUserName>"
        "<FromUserName><![CDATA[fromUser]]></FromUserName>"
        "<CreateTime>1348831860</CreateTime>"
        "<MsgType><![CDATA[text]]></MsgType>"
        "<Content><![CDATA[this is a test]]></Content>"
        "<MsgId>1234567890123456</MsgId>"
        "</xml>"
    )

@pytest.fixture()
def verification_data():
    timestamp = int(time.time())
    nonce = 'TEST_NONCE'
    verification_elements = ['TEST_WECHAT_TOKEN', str(timestamp), nonce]
    verification_elements.sort()
    verification_string = "".join(verification_elements)
    signature = hashlib.sha1(verification_string.encode('utf-8')).hexdigest()
    return {
        'signature': signature,
        'timestamp': timestamp,
        'nonce': nonce,
        'echostr': 'TEST_ECHOSTR'
    }

def test_on_get(client, verification_data):
    query_string = "signature=%s&timestamp=%d&nonce=%s&echostr=%s" % (
        verification_data['signature'],
        verification_data['timestamp'],
        verification_data['nonce'],
        verification_data['echostr']
    )
    result = client.simulate_get('/wechat', query_string=query_string)
    assert result.text == verification_data['echostr']

def test_on_post(client, message):
    result = client.simulate_post('/wechat', body=message)
    parsed_message = xmltodict.parse(result.text)
    assert ('xml' in parsed_message) == True
    assert ('FromUserName' in parsed_message['xml']) == True
    assert ('ToUserName' in parsed_message['xml']) == True
    assert ('Content' in parsed_message['xml']) == True
