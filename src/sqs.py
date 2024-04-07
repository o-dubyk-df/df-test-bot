import asyncio
import json
import logging
import os
from typing import Union

from telegram import Message, Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)
from telegram.ext.filters import FilterDataDict

logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL")

application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()


class TextFilter(filters.MessageFilter):
    __slots__ = ("text",)

    def __init__(self, text: str):
        self.text: str = text
        super().__init__()

    def filter(self, message: Message) -> Union[bool, FilterDataDict] | None:
        if not message.text:
            return False
        return self.text in message.text


async def hello_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )


async def hello_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Hello!"
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Sorry, I don’t understand",
    )


def sqs_handler(event, context):
    logger.info("event: {}".format(json.dumps(event)))
    asyncio.get_event_loop().run_until_complete(main(event))


async def main(event):
    hello_command_handler = CommandHandler("hello", hello_command)
    application.add_handler(hello_command_handler)

    hello_text_handler = MessageHandler(TextFilter("hello") & (~filters.COMMAND), hello_text)
    application.add_handler(hello_text_handler)

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    application.add_handler(echo_handler)

    for record in event["Records"]:
        await application.initialize()
        await application.process_update(
            Update.de_json(json.loads(record["body"]), application.bot)
        )
