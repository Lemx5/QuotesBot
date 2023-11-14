import asyncio
from pyrogram import Client, filters
import wikiquotes
import random
from datetime import datetime, timedelta
import pytz
import os
from flask import Flask

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
        await app.send_message(chat_id, f"{quote}")

# Schedule the task to run twice a day (at 12 AM and 12 PM in Kolkata timezone)
async def schedule_daily_quotes():
    while True:
        now = datetime.now(kolkata_timezone)
        # Set the times for the daily quotes
        morning_time = datetime(now.year, now.month, now.day, hour=0, minute=0, second=0)
        evening_time = datetime(now.year, now.month, now.day, hour=12, minute=0, second=0)
        # Check if it's time for the morning quote
        if now >= morning_time:
            # Calculate the time until the evening
            time_until_evening = (evening_time - now).total_seconds()
            # Wait until the evening
            await asyncio.sleep(time_until_evening)
            # Send the evening quote
            await send_daily_quote()
        # Check if it's time for the evening quote
        elif now >= evening_time:
            # Calculate the time until the next day
            next_day = evening_time + timedelta(days=1)
            time_until_next_day = (next_day - now).total_seconds()
            # Wait until the next day
            await asyncio.sleep(time_until_next_day)
            # Send the morning quote
            await send_daily_quote()

# Start the bot and the scheduled task
if __name__ == "__main__":
    async def main():
        await asyncio.gather(app.start(), schedule_daily_quotes())

    asyncio.run(main())
