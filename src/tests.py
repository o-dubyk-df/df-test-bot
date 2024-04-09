import json
from collections import namedtuple
from unittest import mock, TestCase, IsolatedAsyncioTestCase

from telegram import Bot

from src.api import api_handler, queue
from src.sqs import main as sqs_handler


class APITest(TestCase):

    @mock.patch.object(queue, "send_message")
    def test_success_request(self, queue_mock):
        body = {
            "message": {
                "channel_chat_created": False,

                "text": "hello!",
                "chat": {
                    "first_name": "username",
                    "id": 370810287,
                    "type": "private",
                    "username": "username"
                },
                "date": 1712511740,
                "message_id": 10,
                "from": {
                    "first_name": "username",
                    "id": 370810287,
                    "is_bot": False,
                    "language_code": "en",
                    "username": "username"
                }
            },
            "update_id": 177479048
        }

        event = {"body": json.dumps(body)}
        response = api_handler(event=event, context=mock.Mock())
        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(response["body"], "Success")
        self.assertTrue(queue_mock.is_called())

    @mock.patch.object(queue, "send_message")
    def test_invalid_request(self, queue_mock):
        event = {"body": "test"}
        response = api_handler(event=event, context=mock.Mock())
        self.assertEqual(response["statusCode"], 500)
        self.assertEqual(response["body"], "Invalid JSON payload.")
        self.assertTrue(queue_mock.is_called())


class SQSTestCase(IsolatedAsyncioTestCase):
    event = {
        "message": {
            "text": "/hello",
            "chat": {
                "id": 370810287,
                "type": "private",
            },
            "date": 1712511740,
            "message_id": 10,
        },
        "update_id": 177479048
    }

    @mock.patch.object(Bot, "send_message")
    async def test_input(self, send_mock):
        Case = namedtuple("Case", "msg input output")
        cases = (
            Case(
                msg="hello command",
                input="/hello",
                output="I'm a bot, please talk to me!"
            ),
            Case(
                msg="hello in text",
                input="hellotoyou",
                output="Hello!"
            ),
            Case(
                msg="any text",
                input="abeadmkfdswhelldas",
                output="Sorry, I don’t understand"
            ),
        )

        for case in cases:
            with self.subTest(case.msg):
                self.event["message"]["text"] = case.input
                records = {"Records": [{"body": json.dumps(self.event)}]}
                await sqs_handler(records)
                self.assertTrue(await send_mock.is_called())

                calls = Bot.send_message.call_args_list
                for call in calls:
                    assert call.kwargs["text"] == case.output
