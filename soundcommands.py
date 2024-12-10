from discord.ext import commands
from discord import FFmpegPCMAudio
import os
import asyncio
import random

voice_clients = {}

soundboard_sounds = [
    "fr",
    "i_feel_that",
    "ohhh_paaarth"
]

@commands.command(name='play')
async def play(ctx, sound: str):
    #await ctx.send("AVI BIG NOOB STUPID THENALVR!!!")
    if not ctx.author.voice:
        await ctx.send("Please join a voice channel first!")
        return
    channel = ctx.author.voice.channel

    if ctx.voice_client is None or ctx.voice_client.channel != channel:
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
        vc = await channel.connect()
        voice_clients[channel.id] = vc
        await ctx.send(f"Connected to {channel.name}.")
    else:
        vc = ctx.voice_client

    sound_file = f"./sounds/{sound}.mp3"
    if not os.path.exists(sound_file):
        await ctx.send(f"Sound '{sound}' not found!")
        return

    vc.play(FFmpegPCMAudio(sound_file), after=lambda e: print(f"Finished playing: {sound_file}"))
    await ctx.send(f"Playing: {sound}")

    while vc.is_playing():
        await asyncio.sleep(1)

    if len(channel.members) == 1:
        await vc.disconnect()
        del voice_clients[channel.id]

@commands.command(name='stop')
async def stop(ctx):
    if not ctx.voice_client:
        await ctx.send("I'm not connected to a voice channel!")
        return
    ctx.voice_client.stop()
    await ctx.voice_client.disconnect()
    await ctx.send("Stopped the audio and disconnected.")


@commands.command(name='avi')
async def avi(ctx, duration: int):
    if not ctx.author.voice:
        await ctx.send("Please join a voice channel first!")
        return
    if duration <= 1:
        await ctx.send("Please enter a valid duration!")
        return
    channel = ctx.author.voice.channel
    if ctx.voice_client is None or ctx.voice_client.channel != channel:
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
        vc = await channel.connect()
        voice_clients[channel.id] = vc
        await ctx.send(f"Connected to {channel.name}.")
    else:
        vc = ctx.voice_client
    end_time = asyncio.get_event_loop().time() + duration
    while asyncio.get_event_loop().time() < end_time:
        sound_to_play = random.choice(soundboard_sounds)
        sound_file = f"./sounds/{sound_to_play}.mp3"
        if not os.path.exists(sound_file):
            await ctx.send(f"Sound '{sound_to_play}' not found")
            break
        vc.play(FFmpegPCMAudio(sound_file))
        wait_time = random.randint(5, 20)
        await asyncio.sleep(wait_time)
    if len(channel.members) == 1:
        await vc.disconnect()
        del voice_clients[channel.id]