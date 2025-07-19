import discord
import re
import sqlite3
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

script_dir = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(script_dir, 'data')
DB_NAME = os.path.join(DB_DIR, 'balance2.db')

os.makedirs(DB_DIR, exist_ok=True)

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)
scheduler = AsyncIOScheduler()

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS balance (
            id INTEGER PRIMARY KEY,
            balance REAL
        )''')
        cursor.execute('''INSERT OR IGNORE INTO balance (id, balance)
            VALUES (1, 0.0)''')
        conn.commit()

def get_balance():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM balance WHERE id = 1")
        return cursor.fetchone()[0]

def update_balance(updated_balance):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE balance SET balance = ? WHERE id = 1", (updated_balance,))
        conn.commit()

@client.event
async def on_ready():
    print(f'Bot is online as {client.user}!')
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        balance = get_balance()
        await channel.send(f"💼 Your current balance is: ${balance:.2f}\nBot is online and ready!")
    else:
        print(f"Channel ID {CHANNEL_ID} not found.")

@client.event
async def on_message(message):
    if message.author == client.user or message.channel.id != CHANNEL_ID:
        return

    content = message.content.strip()

    if re.match(r'^[+-]?\d+(\.\d{1,2})?$', content):
        amount = float(content)
        current_balance = get_balance()
        updated_balance = round(current_balance + amount, 2)

        embed = discord.Embed(
            title="💰 Balance Update",
            color=0x00ff00 if amount > 0 else 0xff0000
        )
        embed.add_field(name="Previous Balance", value=f"${current_balance:.2f}", inline=False)
        embed.add_field(
            name="Amount " + ("Added" if amount > 0 else "Subtracted"),
            value=f"${abs(amount):.2f}",
            inline=False
        )
        embed.add_field(name="New Balance", value=f"${updated_balance:.2f}", inline=False)
        embed.set_footer(text="✅ Transaction completed.")

        await message.channel.send(embed=embed)
        update_balance(updated_balance)

    elif content == "!balance":
        balance = get_balance()
        await message.channel.send(f"💼 Your current balance is: ${balance:.2f}")

    else:
        await message.channel.send("ℹ️ Please enter an amount like `+10`, `-5`, or `!balance`.")

# Initialize database and run bot
init_db()

try:
    client.run(TOKEN)
except discord.LoginFailure:
    print("Failed to log in. Check your token.")
except Exception as e:
    print(f"Unexpected error: {e}")
    with open(os.path.join(script_dir, 'script_error.log'), 'a') as log:
        log.write(f"{datetime.now()}: {e}\n")

