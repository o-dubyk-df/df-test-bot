from unittest.mock import AsyncMock
import pytest
from telegram import Bot

from sqs import main


@pytest.fixture
def hello_events():
    return {
        "Records": [
            {
                "body": '{"update_id":813352806,"message":{"message_id":186,"from":{"id":123,"is_bot":false,"first_name":"Test","last_name":"Test","language_code":"uk"},"chat":{"id":123,"first_name":"Test","last_name":"Test","type":"private"},"date":1708367401,"text":"hello"}}'
            },
            {
                "body": '{"update_id":813352806,"message":{"message_id":186,"from":{"id":123,"is_bot":false,"first_name":"Test","last_name":"Test","language_code":"uk"},"chat":{"id":123,"first_name":"Test","last_name":"Test","type":"private"},"date":1708367401,"text":"testhello"}}'
            },
            {
                "body": '{"update_id":813352806,"message":{"message_id":186,"from":{"id":123,"is_bot":false,"first_name":"Test","last_name":"Test","language_code":"uk"},"chat":{"id":123,"first_name":"Test","last_name":"Test","type":"private"},"date":1708367401,"text":"123hello123"}}'
            },
        ]
    }


@pytest.fixture
def hello_command_events():
    return {
        "Records": [
            {
                "body": '{"update_id":813352806,"message":{"message_id":186,"from":{"id":123,"is_bot":false,"first_name":"Test","last_name":"Test","language_code":"uk"},"chat":{"id":123,"first_name":"Test","last_name":"Test","type":"private"},"date":1708367401,"text":"/hello"}}'
            },
            {
                "body": '{"update_id":813352806,"message":{"message_id":186,"from":{"id":123,"is_bot":false,"first_name":"Test","last_name":"Test","language_code":"uk"},"chat":{"id":123,"first_name":"Test","last_name":"Test","type":"private"},"date":1708367401,"text":"!hello"}}'
            },
        ]
    }


@pytest.fixture
def unknown_events():
    return {
        "Records": [
            {
                "body": '{"update_id":813352806,"message":{"message_id":186,"from":{"id":123,"is_bot":false,"first_name":"Test","last_name":"Test","language_code":"uk"},"chat":{"id":123,"first_name":"Test","last_name":"Test","type":"private"},"date":1708367401,"text":"test something"}}'
            },
            {
                "body": '{"update_id":813352806,"message":{"message_id":186,"from":{"id":123,"is_bot":false,"first_name":"Test","last_name":"Test","language_code":"uk"},"chat":{"id":123,"first_name":"Test","last_name":"Test","type":"private"},"date":1708367401,"text":"123123123heellooo123123123"}}'
            },
        ]
    }


@pytest.mark.asyncio
async def test_hello_contain_messages(mocker, hello_events):
    mocker.patch.object(Bot, "send_message", new=AsyncMock())
    mocker.patch.object(Bot, "get_me", new=AsyncMock())

    await main(hello_events, None)

    calls = Bot.send_message.call_args_list
    assert len(calls) == 3
    for call in calls:
        assert call.kwargs["text"] == "Hello!"


@pytest.mark.asyncio
async def test_hello_command(mocker, hello_command_events):
    mocker.patch.object(Bot, "send_message", new=AsyncMock())
    mocker.patch.object(Bot, "get_me", new=AsyncMock())

    await main(hello_command_events, None)

    calls = Bot.send_message.call_args_list
    assert len(calls) == 2  # Only 2 messages contain "/hello" or "!hello"
    for call in calls:
        assert call.kwargs["text"] == "Hello!"


@pytest.mark.asyncio
async def test_hello_unknown(mocker, unknown_events):
    mocker.patch.object(Bot, "send_message", new=AsyncMock())
    mocker.patch.object(Bot, "get_me", new=AsyncMock())

    await main(unknown_events, None)

    calls = Bot.send_message.call_args_list
    assert len(calls) == 2
    assert calls[0].kwargs["text"] == "Sorry, I didn't understand that."
