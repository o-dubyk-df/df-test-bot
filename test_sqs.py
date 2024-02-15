import unittest
from unittest.mock import Mock, AsyncMock, ANY
from telegram import Update
from sqs import hello_command, echo

class TestSQSHandler(unittest.IsolatedAsyncioTestCase):

    async def test_hello_command(self):
        fake_update = Update(update_id=123456789, message=Mock())
        fake_context = Mock()
        fake_context.bot.send_message = AsyncMock()

        await hello_command(fake_update, fake_context)

        fake_context.bot.send_message.assert_called_once()
        fake_context.bot.send_message.assert_called_with(chat_id=ANY, text="world")


    async def test_echo_command_hello(self):

        fake_message_hello = Mock(text="hello", chat_id=123)
        fake_update_hello = Update(update_id=123456789, message=fake_message_hello)
        fake_context_hello = Mock()
        fake_context_hello.bot.send_message = AsyncMock()

        await echo(fake_update_hello, fake_context_hello)
        fake_context_hello.bot.send_message.assert_called_with(chat_id=ANY, text="world")

    async def test_echo_command_another_word(self):

        fake_message_other = Mock(text="test", chat_id=123)
        fake_update_other = Update(update_id=123456789, message=fake_message_other)
        fake_context_other = Mock()
        fake_context_other.bot.send_message = AsyncMock()

        await echo(fake_update_other, fake_context_other)
        fake_context_other.bot.send_message.assert_called_with(chat_id=ANY, text="I don't understand")


if __name__ == '__main__':
    unittest.main()