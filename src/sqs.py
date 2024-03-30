import json
import asyncio
from typing import Union
from telegram import Message, Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)
import logging
import os
from telegram.ext.filters import FilterDataDict

logger = logging.getLogger()
logger.setLevel(logging.INFO)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", default="")
SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL")

application = (
    ApplicationBuilder().token("6618775489:AAGpLKPHqfo8hqhU_JnasjGDLrSAjck6FXo").build()
)


class TextContainsFilter(filters.MessageFilter):
    __slots__ = ("text",)

    def __init__(self, text: str):
        self.text: str = text
        super().__init__(
            name=f"filters.TextContainsFilter({text})" if text else "filters.TEXT"
        )

    def filter(self, message: Message) -> Union[bool, FilterDataDict] | None:
        if not message.text:
            return False
        return self.text in message.text


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_chat:
        return
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello")


async def echo_hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_chat:
        return
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello!")


async def echo_unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_chat:
        return
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Sorry, I didn't understand that."
    )


def lambda_handler(event, context):
    logger.info("event: {}".format(json.dumps(event)))

    asyncio.get_event_loop().run_until_complete(main(event, context))


async def main(event, context):
    hello_handler = CommandHandler("hello", hello)
    application.add_handler(hello_handler)

    echo_handler = MessageHandler(
        TextContainsFilter("hello") & (~filters.COMMAND), echo_hello
    )
    application.add_handler(echo_handler)

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo_unknown)
    application.add_handler(echo_handler)

    for record in event["Records"]:
        await application.initialize()
        await application.process_update(
            Update.de_json(json.loads(record["body"]), application.bot)
        )
