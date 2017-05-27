import pytest

from webmock import mock_server
from lib.wechat.wechatqueueprocessor import WeChatQueueProcessor

mock_server_calls_count = 0

@pytest.fixture()
def queue_processor():
    return WeChatQueueProcessor('TEST_APP_ID', 'TEST_APP_SECRET')

@pytest.fixture()
def message():
    return {
        'sender': 'fromUser',
        'receiver': 'toUser',
        'type': 'text',
        'content': 'this is a test',
        'valid': True
    }

def mock_token_request_success(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'application/json')]
    start_response(status, headers)
    return ['{"access_token":"TEST_ACCESS_TOKEN","expires_in":7200}'.encode('utf-8')]

def mock_token_request_error(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'application/json')]
    start_response(status, headers)
    return ['{"errcode":40013,"errmsg":"invalid appid"}'.encode('utf-8')]

def mock_send_message_request_success(environ, start_response):
    global mock_server_calls_count
    status = '200 OK'
    headers = [('Content-type', 'application/json')]
    start_response(status, headers)
    if mock_server_calls_count == 0:
        response_body = '{"access_token":"TEST_ACCESS_TOKEN","expires_in":7200}'
        mock_server_calls_count = 1
    else:
        response_body = '{"errcode":0}'

    return [response_body.encode('utf-8')]

def mock_send_message_request_error(environ, start_response):
    global mock_server_calls_count
    status = '200 OK'
    headers = [('Content-type', 'application/json')]
    start_response(status, headers)
    if mock_server_calls_count == 0:
        response_body = '{"access_token":"TEST_ACCESS_TOKEN","expires_in":7200}'
        mock_server_calls_count = 1
    else:
        response_body = '{"errcode":40013,"errmsg":"invalid appid"}'

    return [response_body.encode('utf-8')]

def test_get_access_token_success(queue_processor):
    with mock_server(mock_token_request_success) as port:
        test_server_url = 'http://127.0.0.1:{}'.format(port)
        queue_processor.WECHAT_URL = test_server_url
        token_result = queue_processor.get_access_token()
        assert token_result != None
        assert token_result == 'TEST_ACCESS_TOKEN'

def test_get_access_token_error(queue_processor):
    with mock_server(mock_token_request_error) as port:
        test_server_url = 'http://127.0.0.1:{}'.format(port)
        queue_processor.WECHAT_URL = test_server_url
        token_result = queue_processor.get_access_token()
        assert token_result == None

def test_process_message_success(queue_processor, message):
    mock_server_calls_count = 0
    with mock_server(mock_send_message_request_success) as port:
        test_server_url = 'http://127.0.0.1:{}'.format(port)
        queue_processor.WECHAT_URL = test_server_url
        send_result = queue_processor.process_message(message)
        assert send_result == True

def test_process_message_error(queue_processor, message):
    mock_server_calls_count = 0
    with mock_server(mock_send_message_request_error) as port:
        test_server_url = 'http://127.0.0.1:{}'.format(port)
        queue_processor.WECHAT_URL = test_server_url
        send_result = queue_processor.process_message(message)
        assert send_result == False
