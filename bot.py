import os
from pyrogram import Client, filters
import wikiquotes
from flask import Flask
from threading import Thread
import random
import asyncio
import aiohttp

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client(
    "qoutesbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# list of adjectives
indexs = [
    "Motivation", "Inspiration", "Consistency", "Quotes", "Education", "Encourage",
    "Love", "Care", "Romantic", "Beautiful", "Respect", "Humanity", "Life", "Afterlife",
    "Determination", "Perseverance", "Dedication", "Success", "Wisdom", "Faith", "Courage",
    "Hope", "Passion", "Gratitude", "Joy", "Harmony", "Serenity", "Positivity", "Growth",
    "Patience", "Resilience", "Dream", "Believe", "Achieve", "Empower", "Thrive", "Connection",
    "Balance", "Innerpeace", "Enlightenment", "Kindness", "Compassion", "Generosity",
    "Forgiveness", "Grace", "Spirituality", "Transformation", "Legacy", "Purpose", "Eternity",
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

# list of popular authors & personalities
authers = [
    "Zig Ziglar", "Dale Carnegie", "Stephen R. Covey", "Napoleon Hill", "Jim Rohn",
    "Brian Tracy", "Eric Thomas", "Les Brown", "Jack Canfield", "Mark Manson",
    "Albert Einstein", "Mahatma Gandhi", "Marie Curie", "Nelson Mandela", "Leonardo da Vinci",
    "Coco Chanel", "Martin Luther King Jr.", "Steve Jobs", "Malala Yousafzai", "Oprah Winfrey",
    "Abraham Lincoln", "Mother Teresa", "Bill Gates", "Rosa Parks", "Winston Churchill",
    "Jane Goodall", "Pablo Picasso", "Billie Jean King", "Elon Musk", "Aung San Suu Kyi",
    "Charles Darwin", "Walt Disney", "Martha Graham", "Mao Zedong", "George Washington",
    "Sigmund Freud", "Frederick Douglass", "Anne Frank", "Katherine Johnson", "Vincent van Gogh",
    "Wright Brothers", "Margaret Thatcher", "Bob Dylan", "Harriet Tubman", "Desmond Tutu",
    "Helen Keller", "Michael Jordan", "Socrates", "Aristotle", "Confucius", "Joan of Arc", "Cleopatra",
    "Thomas Edison", "Amelia Earhart", "John F. Kennedy", "Muhammad Ali", "Pele",
    "Harper Lee", "John Lennon", "Paul McCartney", "Ravi Shankar", "Queen Elizabeth II",
    "Harriet Beecher Stowe", "Sylvia Plath", "Roald Amundsen", "Neil Armstrong", "Buzz Aldrin",
    "Hedy Lamarr", "Grace Hopper", "Emmeline Pankhurst", "Sojourner Truth", "Ada Lovelace",
    "Frederick Banting", "Louis Pasteur", "Marie Antoinette", "Diana, Princess of Wales", "John Locke",
    "Eleanor Roosevelt", "Ronald Reagan", "Harold Pinter", "Frida Kahlo", "Diego Rivera",
    "Isaac Newton", "Mikhail Gorbachev", "Babe Ruth", "Pablo Neruda", "Deng Xiaoping",
    "Vladimir Putin", "Aristotle Onassis", "Immanuel Kant", "Marilyn Monroe", "Rosalind Franklin",
    "Marlon Brando", "Walt Whitman", "James Cameron", "Salvador Dalí", "Martha Stewart",
    "Fidel Castro", "Anne Hathaway", "Charlie Chaplin", "Leo Messi", "Michael Phelps",
    "George Lucas", "Fidel Castro", "Dolly Parton", "Stephen Hawking", "J.K. Rowling",
    "Isaac Asimov", "Richard Feynman", "Jane Goodall", "Toni Morrison", "Oscar Wilde",
    "Ralph Waldo Emerson", "Robert Frost", "T.S. Eliot", "Sylvia Plath", "Maya Angelou",
    "James Baldwin", "Gabriel García Márquez", "Fidel Castro", "Dalai Lama", "Paulo Coelho",
    "Salman Rushdie", "Kazuo Ishiguro", "Mozart", "Beethoven", "Elvis Presley",
    "The Beatles", "David Bowie", "Michael Jackson", "Bob Marley", "Freddie Mercury",
    "Winston Churchill", "Coco Chanel", "Billie Holiday", "Ella Fitzgerald", "Louis Armstrong",
    "Aretha Franklin", "James Brown", "Ray Charles", "Prince", "Stevie Wonder", "Jimi Hendrix",
    "Frank Sinatra", "Miles Davis", "John Coltrane", "Duke Ellington", "Nat King Cole",
    "Marvin Gaye", "Sam Cooke", "Whitney Houston", "Barbra Streisand", "Maria Callas",
    "Luciano Pavarotti", "Enrico Caruso", "Johann Sebastian Bach", "Ludwig van Beethoven",
    "Apj Abdul Kalam", "Swami Vivekananda", "Sri Aurobindo", "Rabindranath Tagore", "Mahatma Gandhi",
    "Mother Teresa", "Sardar Vallabhbhai Patel", "Jawaharlal Nehru", "Subhas Chandra Bose",
    "Bhagat Singh", "Lal Bahadur Shastri", "Indira Gandhi", "Rajiv Gandhi", "Atal Bihari Vajpayee",
    "Manmohan Singh", "Narendra Modi", "Sachin Tendulkar", "Milkha Singh", "Mary Kom",
    "Saina Nehwal", "P. V. Sindhu", "Vishwanathan Anand", "Kapil Dev", "Sunil Gavaskar",
]

# To fetch random Quotes
async def fetch_quote_content():
    url = "https://api.quotable.io/quotes/random"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                quote_data = await response.json()
                
                # Check if the response is a list of quotes
                if isinstance(quote_data, list) and len(quote_data) > 0:
                    quote = quote_data[0]
                    return quote.get("content", None), quote.get("author", None)
                
                # If not a list, assume it's a single quote
                return quote_data.get("content", None), quote_data.get("author", None)
            else:
                print(f"Error: Unable to fetch quote. Status code: {response.status}")
                return None, None


@app.on_message(filters.command("quotes"))
async def send_quote(_, message):
    quote_content, quote_author = await fetch_quote_content()
    auther = quote_author.replace(" ", "_")
    await message.reply(f'<code>{quote_content}</code>\n~ <b><a href="https://en.wikiquote.org/wiki/{auther}">{quote_author}</a></b>', disable_web_page_preview=True)

@app.on_message(filters.command("start") & filters.private)
async def start(_, message):
    await message.reply(f"<b>Hi {message.from_user.mention}!\nI'm a bot that sends quotes, Send me author's name to get a quote from them or send</b> /quotes")

@app.on_message(filters.command("qotd") & filters.private)
async def send_quote_of_the_day(client, message):
    quote = wikiquotes.quote_of_the_day("english")
    await message.reply(f"<code>{quote}</code>")

@app.on_message(filters.command("random") & filters.private)
async def send_random_quote(_, message):
    adj = random.choice(indexs)
    quote = wikiquotes.random_quote(adj, "english")
    await message.reply(f'<code>{quote}</code>\n<b>~ <a href="https://telegram.me/QuotyRoBot">{adj}</a></b>', disable_web_page_preview=True)

@app.on_message(filters.command("authors") & filters.private)
async def send_author_quote(_, message):
    people = random.choice(authers)
    pubs = people.replace(" ", "_")
    quote = wikiquotes.random_quote(people, "english")
    await message.reply(f'<code>{quote}</code>\n~ <b><a href="https://en.wikiquote.org/wiki/{pubs}">{people}</a></b>', disable_web_page_preview=True)

@app.on_message(filters.text & filters.private)
async def random_quotes(_, message):
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
