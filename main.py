import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Loads environment variables from .env
load_dotenv()

# Define intents
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.messages = True
intents.message_content = True
intents.voice_states = True
intents.reactions = True

# Creates bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


# Test command
@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Please use a valid command.")


# Starts the bot
bot.run(os.getenv('TOKEN'))
