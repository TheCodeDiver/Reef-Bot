import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()

# Define intents
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.messages = True
intents.message_content = True
intents.voice_states = True
intents.reactions = True

# Create bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user}')

async def load_extensions():
    await bot.load_extension("cogs.task_tracker")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(os.getenv('TOKEN'))

asyncio.run(main())
