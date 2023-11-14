import os
import asyncio
from pyrogram import Client, filters
import wikiquotes
import random
from datetime import datetime, timedelta
import pytz
from quart import Quart, jsonify

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = os.getenv("CHANNEL")

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

kolkata_timezone = pytz.timezone("Asia/Kolkata")

app = Quart(__name__)
pyro_client = Client(
    "qoutesbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


def get_random_quote():
    author_name = random.choice(authors_and_hashtags)
    try:
        quote = wikiquotes.random_quote(author_name, "english")
        return quote
    except Exception as e:
        print(f"Error fetching quote: {e}")
        return None


async def send_daily_quote():
    chat_id = CHANNEL
    quote = get_random_quote()
    if quote:
        await pyro_client.send_message(chat_id, f"<code>{quote}</code>")


async def schedule_daily_quotes():
    while True:
        now = datetime.now(kolkata_timezone)
        morning_time = kolkata_timezone.localize(datetime(now.year, now.month, now.day, hour=0, minute=0, second=0))
        evening_time = kolkata_timezone.localize(datetime(now.year, now.month, now.day, hour=12, minute=0, second=0))

        if now >= morning_time:
            time_until_evening = (evening_time - now).total_seconds()
            await asyncio.sleep(time_until_evening)
            asyncio.create_task(send_daily_quote())
        elif now >= evening_time:
            next_day = evening_time + timedelta(days=1)
            time_until_next_day = (next_day - now).total_seconds()
            await asyncio.sleep(time_until_next_day)
            asyncio.create_task(send_daily_quote())


@pyro_client.on_message(filters.command("start") & filters.private)
async def start(_, message):
    await message.reply("Hi there! I'm a bot that sends quotes\n\n Send me author's name to get a quote from them")


@pyro_client.on_message(filters.text & filters.private)
async def send_quote(_, message):
    author = message.text
    quote = wikiquotes.random_quote(author, "english")
    await message.reply(f"<code>{quote}</code>")


@app.route("/", methods=["GET"])
async def home():
    return jsonify({"status": "Alive"})


async def run_web_app():
    await app.run_task(host="0.0.0.0", port=8080)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(schedule_daily_quotes())
    loop.create_task(run_web_app())
    loop.run_until_complete(pyro_client.start())
    loop.run_until_complete(pyro_client.idle())
