from discord.ext import commands
import os

@commands.command(name='addsound')
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

@commands.command(name='connect')
async def connect(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        if ctx.voice_client:
            await ctx.send(f"Already connected to {ctx.voice_client.channel.name}.")
            await ctx.voice_client.disconnect()
            return
        await channel.connect()
        await ctx.send(f"Connected to {channel.name}.")
    else:
        await ctx.send("You need to join a voice channel first.")

@commands.command(name="list_commands")
async def list_commands(ctx):
    command_list = [
        ("!addsound <file>", "Add a sound to the soundboard. Usage: !addsound <file> (attach an mp3 or wav file)"),
        ("!connect", "Connect to a voice channel. Usage: !connect"),
        ("!play <sound>", "Play a sound from the soundboard. Usage: !play <sound> (e.g., !play fein)"),
        ("!stop", "Stop the currently playing sound. Usage: !stop"),
        ("!avi <duration>", "Summon Avi for a given duration in seconds. Usage: !avi <duration> (e.g., !avi 30)"),
        ("!stream <query or url>", "Stream a song or video from Youtube. Usage: !stream <query> (e.g., !stream Parthena Type of Love (Romanized Hangul) Eng Version feat. Ken Carson)"),
        ("!skip", "Skip the current song or video that is streaming (Prolly whatever Hritik added to the queue). Usage: !skip"),
        ("!list_commands", "Show this list of commands. Usage: !commands")
    ]
    response = "Here are all the available commands: \n\n"
    for command, description in command_list:
        response += f"**{command}: **{description}\n"
    await ctx.send(response)