import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import yt_dlp
import asyncio
from collections import deque

ytdl_format_options = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'noplaylist':True,
    'cookies': '/home/opc/Soundboard/cookies.txt',
    'verbose': True
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

ffmpeg_options = {
    'options': '-vn'
}

voice_clients = {}
song_queues = {}

async def play_next(ctx, channel_id):
    if channel_id in song_queues and song_queues[channel_id]:
        next_song = song_queues[channel_id].popleft()
        vc = voice_clients.get(channel_id)
        if vc and next_song:
            vc.play(FFmpegPCMAudio(next_song['url'], **ffmpeg_options),
                    after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx, channel_id), asyncio.get_event_loop()))
            await ctx.send(f"Now playing: {next_song['title']}")
    else:
        vc = voice_clients.get(channel_id)
        if vc:
            await vc.disconnect()
            del voice_clients[channel_id]

@commands.command(name='stream')
async def stream(ctx, *, query: str):
    if not ctx.author.voice:
        await ctx.send("Join a voice channel first!")
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
    try:
        await ctx.send(f"Searching for: {query}")
        if not ("youtube.com" in query or "youtu.be" in query or "https:" in query):
            search_opts = {
                'format': 'bestaudio/best',
                'noplaylist': True,
                'quiet': True,
                'default_search': 'ytsearch',
            }
            with yt_dlp.YoutubeDL(search_opts) as ydl:
                info = ydl.extract_info(query, download=False)
                if 'entries' in info:
                    info = info['entries'][0]
        else:
            info = ytdl.extract_info(query, download=False)

        song = {
            'url': info['url'],
            'title': info.get('title', 'Unknown Title'),
            'user': f"{ctx.author.name}#{ctx.author.discriminator}"
        }
        if channel.id not in song_queues:
            song_queues[channel.id] = deque()
        song_queues[channel.id].append(song)
        await ctx.send(f"Added to queue: {song['title']} (added by {song['user']})")

        if not vc.is_playing():
            await play_next(ctx, channel.id)

        if len(channel.members) <= 1:
            await vc.disconnect()
            del voice_clients[channel.id]

    except Exception as e:
        await ctx.send("An error occured :(")
        print(f"Error:{e}")

@commands.command(name='skip')
async def skip(ctx):
    channel = ctx.author.voice.channel
    vc = ctx.voice_client
    if not vc:
        await ctx.send("Not connected to a voice channel.")
        return
    if vc.is_playing():
        vc.stop()
        await ctx.send("Skipping current song...")

        if channel.id in song_queues and song_queues[channel.id]:
            await play_next(ctx, channel.id)
        else:
            await ctx.send("No more songs in the queue.")
    else:
        await ctx.send("No current songs playing!")