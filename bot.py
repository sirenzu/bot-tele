import logging
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import requests
from bs4 import BeautifulSoup
import yt_dlp

# Set up logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    level=logging.INFO)
logger = logging.getLogger("bkpranbot")

# Set your bot token (via environment variables)
TOKEN_BOT = '7617338678:AAGIiXBYiMZ2SQzag1ZsjkxaxABHMfZdb-g'  # Ganti dengan token bot kamu

# Load token count data
def load_token_data():
    try:
        with open("data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save token data
def save_token_data(data):
    with open("data.json", "w") as file:
        json.dump(data, file)

# Start command to greet users
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    data = load_token_data()
    if user_id not in data:
        data[user_id] = {"tokens": 50}  # Initial 50 tokens
        save_token_data(data)
    await update.message.reply("Welcome! You have 50 tokens. Send a request to get a video!")

# Function to search and fetch video based on user request
async def fetch_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    request = update.message.text.strip()

    data = load_token_data()
    if user_id not in data or data[user_id]["tokens"] <= 0:
        await update.message.reply("Sorry, you don't have enough tokens. Please top up.")
        return

    # Decrease token count for the user
    data[user_id]["tokens"] -= 5  # Each video request costs 5 tokens
    save_token_data(data)

    # Search for video (this is an example, you can adjust to fetch from other sites)
    video_url = f"https://www.xnxx.com/video_search/{request}"

    # Scrape the video URL
    response = requests.get(video_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    video = soup.find('video')

    if video:
        video_src = video['src']
        await update.message.reply(f"Here's the video you requested: {video_src}")
    else:
        await update.message.reply("No video found for your request.")

# Main function to start the bot
async def main():
    application = Application.builder().token(TOKEN_BOT).build()

    # Command handler
    application.add_handler(CommandHandler("start", start))

    # Message handler for video requests
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fetch_video))

    await application.run_polling()

if "bkpranbot" == "_main_":
    import asyncio
    asyncio.run(main())