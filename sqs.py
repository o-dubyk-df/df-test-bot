import json
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_BOT_TOKEN = '6972948262:AAFGErnB6zzpKSZz1vUFdD1ceyqBuQN4eXY'
SQS_QUEUE_URL = os.getenv('SQS_QUEUE_URL')

application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

async def hello_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="world")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if 'hello' in text:
        text_answer="world"
    else:
        text_answer="I don't understand"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_answer)

def lambda_handler(event, context):
    logger.info("event: {}".format(json.dumps(event)))
    asyncio.get_event_loop().run_until_complete(main(event, context))

async def main(event, context):
    start_handler = CommandHandler('hello', hello_command)
    application.add_handler(start_handler)
    
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    application.add_handler(echo_handler)
    
    for record in event['Records']:
        await application.initialize()
        await application.process_update(
            Update.de_json(json.loads(record["body"]), application.bot)
        )
   