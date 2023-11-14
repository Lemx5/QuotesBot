import os
from pyrogram import Client, filters
import wikiquotes
from flask import Flask
from threading import Thread
import random

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client(
    "qoutesbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


indexs = [
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
    "Tony Robbins", "Oprah Winfrey", "Sheryl Sandberg", "Elon Musk", "Warren Buffett",
    "Richard Branson", "Malala Yousafzai", "Maya Angelou", "Steve Jobs", "Michelle Obama",
    "Innovation", "Creativity", "Leadership", "Motivational", "Self-improvement", "Mindfulness",
    "Grit", "Ambition", "Optimism", "Self-discovery", "Empathy", "Unity", "Inclusivity", "Harmony",
    "Health", "Wellness", "Fitness", "Nutrition", "Mindset", "Adventure", "Exploration", "Discovery",
    "Adaptability", "Change", "Challenges", "Reflection", "Laughter", "Friendship", "Family",
    "Community", "Collaboration", "Teamwork", "Innovation", "Learning", "Knowledge", "Curiosity",
    "Open-mindedness", "Wisdom", "Reflection", "Mindfulness", "Purpose", "Legacy", "Impact", "Gratitude",
    "Happiness", "Joy", "Peace", "Optimism", "Courage", "Authenticity", "Resilience", "Kindness",
    "Compassion", "Generosity", "Forgiveness", "Empowerment", "Transformation", "Simplicity", "Balance",
    "Nature", "Environment", "Sustainability", "Philanthropy", "Global", "Diversity", "Equality", "Justice",
    "Peace", "Calmness", "Adventure", "Discovery", "Wonder", "Imagination", "Curiosity", "Boldness",
    "Risk-taking", "Resourcefulness", "Vision", "Clarity", "Focus", "Discipline", "Consistency", "Action",
    "Reflection", "Adaptability", "Integrity", "Authenticity", "Authenticity", "Mindfulness",
]

@app.on_message(filters.command("start") & filters.private)
async def start(_, message):
    await message.reply(f"<b>Hi {message.from_user.mention}!\nI'm a bot that sends quotes, Send me author's name to get a quote from them or send</b> /random")

@app.on_message(filters.command("quote") & filters.private)
async def send_quote_of_the_day(client, message):
    quote = wikiquotes.quote_of_the_day("english")
    await message.reply(f"<code>{quote}</code>")

@app.on_message(filters.command("random") & filters.private)
async def send_random_quote(_, message):
    author = random.choice(indexs)
    quote = wikiquotes.random_quote(author, "english")
    await message.reply(f"<code>{quote}</code>\n~ <b>#{author}</b>")

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
