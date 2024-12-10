from typing import Final
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

from soundcommands import play, stop, avi
from generalcommands import addsound, connect, list_commands
from streamcommands import stream, skip
#from discord import FFmpegPCMAudio
#from discord import Intents, Client, Message
#from responses import get_response
#import asyncio

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

#print(discord.__version__)

#setup
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.voice_states = True
intents.guild_messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# Register the commands
bot.add_command(play)
bot.add_command(stop)
bot.add_command(addsound)
bot.add_command(connect)
bot.add_command(stream)
bot.add_command(avi)
bot.add_command(skip)
bot.add_command(list_commands)

bot.run(TOKEN)