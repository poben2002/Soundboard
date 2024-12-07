from typing import Final
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord import Intents, Client, Message
from responses import get_response
import asyncio

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

print(discord.__version__)

#setup
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.voice_states = True
intents.guild_messages = True

voice_clients = {}
bot = commands.Bot(command_prefix="!", intents=intents)

#Sound command
@bot.command(name='play')
async def play(ctx, sound: str):
    if not ctx.author.voice:
        await ctx.send("Please join a voice channel first!")
        return

    channel = ctx.author.voice.channel
    #if not bot.voice_clients:
    #    vc = await channel.connect()
    #else:
    #    vc = bot.voice_clients[0]

    sound_file = f"./sounds/{sound}.mp3"
    if not os.path.exists(sound_file):
        await ctx.send(f"Sound '{sound}' not found!")
        return

    if channel.id not in voice_clients:
        vc = await channel.connect()
        voice_clients[channel.id] = vc
    else:
        vc = voice_clients[channel.id]

    vc.play(FFmpegPCMAudio(sound_file), after=lambda e: print(f"Finished playing: {sound_file}"))
    await ctx.send(f"Playing: {sound}")

    while vc.is_playing():
        await asyncio.sleep(1)

    if len(channel.members) == 1:
        await vc.disconnect()
        del voice_clients[channel.id]

@bot.command(name='stop')
async def stop(ctx):
    if not ctx.voice_client:
        await ctx.send("I'm not connected to a voice channel!")
        return
    ctx.voice_client.stop()
    await ctx.voice_client.disconnect()
    await ctx.send("Stopped the audio and disconnected.")

@bot.command(name='addsound')
async def addsound(ctx):
    if len(ctx.message.attachments) == 0:
        await ctx.send("Please attach a sound file!")
        return
    attachment = ctx.message.attachments[0]
    filename = attachment.filename
    if not filename.endswith(('.mp3', '.wav')):
        await ctx.send("Please send a valid sound file (type mp3 or wav)!")
        return
    save_path = f"./sounds/{filename}"
    await attachment.save(save_path)
    await ctx.send(f"Sound '{filename}' added successfully!")

#Bot ready event
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
bot.run(TOKEN)