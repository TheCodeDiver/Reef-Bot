import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Define intents (equivalent to JS version)
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.messages = True
intents.message_content = True
intents.voice_states = True
intents.reactions = True

# Create bot instance (using commands.Bot even if no commands yet)
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


# Add your command here, outside of on_ready
@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Please use a valid command.")


# Start the bot using the token from .env
bot.run(os.getenv('TOKEN'))
