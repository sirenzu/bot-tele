import logging
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Token bot kamu
TOKEN_BOT = '7617338678:AAGIiXBYiMZ2SQzag1ZsjkxaxABHMfZdb-g'

def load_token_data():
    try:
        with open("data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_token_data(data):
    with open("data.json", "w") as file:
        json.dump(data, file)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    data = load_token_data()
    if user_id not in data:
        data[user_id] = {"tokens": 50}
        save_token_data(data)
    await update.message.reply_text("Welcome! You have 50 tokens. Send a keyword to search for a video.")

async def fetch_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    request = update.message.text.strip()
    data = load_token_data()

    if user_id not in data or data[user_id]["tokens"] < 5:
        await update.message.reply_text("Not enough tokens. Please top up.")
        return

    # Simulasi respons video (belum real ambil dari web)
    data[user_id]["tokens"] -= 5
    save_token_data(data)

    await update.message.reply_text(f"Request '{request}' received. (Video fetching not yet implemented.)")

async def main():
    application = Application.builder().token(TOKEN_BOT).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fetch_video))
    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
