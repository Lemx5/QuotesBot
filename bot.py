import os
import asyncio
from pyrogram import Client, filters
import wikiquotes
from flask import Flask
from threading import Thread

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client(
    "qoutesbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


@app.on_message(filters.command("start") & filters.private)
async def start(_, message):
    await message.reply("Hi there! I'm a bot that sends quotes\n\n Send me author's name to get a quote from them")


@app.on_message(filters.text & filters.private)
async def send_quote(_, message):
    author = message.text
    quote = wikiquotes.random_quote(author, "english")
    await message.reply(f"<code>{quote}</code>")


# Flask configuration
web = Flask(__name__)

@web.route('/')
def index():
    return "Bot is running!"

def run():
    web.run(host="0.0.0.0", port=int(os.environ.get('PORT', 8080)))

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    app.run()      
