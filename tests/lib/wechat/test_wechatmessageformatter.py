import pytest
import xmltodict

from lib.wechat.wechatmessageformatter import WeChatMessageFormatter

@pytest.fixture()
def message_formatter():
    return WeChatMessageFormatter()

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

def test_parse_incoming_message(message_formatter, message):
    parsed_message = message_formatter.parse_incoming_message(message)
    assert ('valid' in parsed_message) == True
    assert parsed_message['valid'] == True

def test_validate_incoming_message(message_formatter, message):
    parsed_message = xmltodict.parse(message)
    validation_result = message_formatter.validate_incoming_message(parsed_message)
    assert validation_result == True
