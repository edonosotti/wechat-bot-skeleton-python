import pytest
import xmltodict

from lib.wechat.wechatmessageformatter import WeChatMessageFormatter

@pytest.fixture()
def message_formatter():
    return WeChatMessageFormatter()

@pytest.fixture()
def incoming_message():
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
def parsed_message():
    return {
        'sender': 'fake-sender',
        'receiver': 'fake-receiver',
        'type': 'text',
        'content': 'test-message',
        'valid': True
    }

def test_parse_incoming_message(message_formatter, incoming_message):
    parsed_message = message_formatter.parse_incoming_message(incoming_message)
    assert ('valid' in parsed_message) == True
    assert parsed_message['valid'] == True

def test_validate_incoming_message(message_formatter, incoming_message):
    parsed_message = xmltodict.parse(incoming_message)
    validation_result = message_formatter.validate_incoming_message(parsed_message)
    assert validation_result == True

def test_format_instant_reply(message_formatter, parsed_message):
    reply_message = 'test-reply'
    instant_reply = message_formatter.format_instant_reply(parsed_message, reply_message)
    parsed_reply = xmltodict.parse(instant_reply)
    assert 'xml' in parsed_reply
    assert 'Content' in parsed_reply['xml']
    assert parsed_reply['xml']['Content'] == reply_message

def test_format_delayed_reply(message_formatter, parsed_message):
    reply_message = 'test-reply'
    instant_reply = message_formatter.format_delayed_reply(parsed_message, reply_message)
    assert 'text' in instant_reply
    assert 'content' in instant_reply['text']
    assert instant_reply['text']['content'] == reply_message
