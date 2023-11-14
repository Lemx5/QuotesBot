import asyncio
from pyrogram import Client, filters
import wikiquotes
import random
from datetime import datetime, timedelta
import pytz
import os
from quart import Quart

# Set up your Pyrogram API credentials
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = os.getenv("CHANNEL")

# List of authors and hashtags combined
authors_and_hashtags = [
    "Zig Ziglar", "Dale Carnegie", "Stephen R. Covey", "Napoleon Hill", "Jim Rohn",
    "Brian Tracy", "Eric Thomas", "Les Brown", "Jack Canfield", "Mark Manson",
    "Simon Sinek", "Gary Vaynerchuk", "Mel Robbins", "Grant Cardone", "Robin Sharma",
    "Motivation", "Inspiration", "Consistency", "Quotes", "Education", "Encourage",
    "Love", "Care", "Romantic", "Beautiful", "Respect", "Humanity", "Life", "Afterlife",
    "Determination", "Perseverance", "Dedication", "Success", "Wisdom", "Faith", "Courage",
    "Hope", "Passion", "Gratitude", "Joy", "Harmony", "Serenity", "Positivity", "Growth",
    "Patience", "Resilience", "Dream", "Believe", "Achieve", "Empower", "Thrive", "Connection",
    "Balance", "Innerpeace", "Enlightenment", "Kindness", "Compassion", "Generosity",
    "Forgiveness", "Grace", "Spirituality", "Transformation", "Legacy", "Purpose", "Eternity",
]

# Set the timezone for Kolkata
kolkata_timezone = pytz.timezone("Asia/Kolkata")

# Create a Pyrogram Client
app = Client(
    "qoutesbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN)

# Function to get a random quote using wikiquotes
def get_random_quote():
    author_name = random.choice(authors_and_hashtags)
    try:
        quote = wikiquotes.random_quote(author_name, "english")
        return quote
    except Exception as e:
        print(f"Error fetching quote: {e}")
        return None

# Function to send a quote to the Telegram channel
async def send_daily_quote():
    chat_id = CHANNEL
    quote = get_random_quote()
    if quote:
        await app.send_message(chat_id, f"<code>{quote}</code>")

# Schedule the task to run twice a day (at 12 AM and 12 PM in Kolkata timezone)
async def schedule_daily_quotes():
    while True:
        now = datetime.now(kolkata_timezone)
        
        # Explicitly assign timezone to morning_time and evening_time
        morning_time = kolkata_timezone.localize(datetime(now.year, now.month, now.day, hour=0, minute=0, second=0))
        evening_time = kolkata_timezone.localize(datetime(now.year, now.month, now.day, hour=12, minute=0, second=0))

        if now >= morning_time:
            time_until_evening = (evening_time - now).total_seconds()
            asyncio.create_task(asyncio.sleep(time_until_evening))
            asyncio.create_task(send_daily_quote())
        elif now >= evening_time:
            next_day = evening_time + timedelta(days=1)
            time_until_next_day = (next_day - now).total_seconds()
            asyncio.create_task(asyncio.sleep(time_until_next_day))
            asyncio.create_task(send_daily_quote())


@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply("Hi there! I'm a bot that sends quotes\n\n Send me author's name to get a quote from them")

@app.on_message(filters.text & filters.private)
async def send_quote(client, message):
    author = message.text
    quote = wikiquotes.random_quote(author, "english")
    await message.reply(f"<code>{quote}</code>") 

# Flask configuration
web = Quart(__name__)

# Web app routes & home page
@web.route("/", methods=["GET"])            
async def home():
    return "Bot is running!"

# Run the web app
async def run_web_app():
    await web.run_task(host="0.0.0.0", port=8080)         

# Start the bot and Flask simultaneously
# Start the bot and web app
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(schedule_daily_quotes())
    loop.create_task(run_web_app())
    app.run()