import os
import discord
import yt_dlp

from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import Context
from pytube import YouTube

from utils import youtube_url_validation

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': '%(id)s.%(ext)s',
    'quiet': True,
    'no_warnings': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

load_dotenv(dotenv_path="./.env")
TOKEN = os.getenv('TOKEN')

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.command()
async def p(ctx: Context, arg):
    if not (url := youtube_url_validation(arg)):
        return
    url = url.group(0)

    if not ctx.author.voice:
        await ctx.channel.send("Moras biti u voice kanalu prvo")
        return

    try:
        yt = YouTube(url)
        title = yt.title
    except:
        await ctx.channel.send("Nmg da ucitam, posalji opet mozda")
        return
    
    if not bot.voice_clients:
        try:
            voice_client = await ctx.author.voice.channel.connect()
        except:
            await ctx.channel.send(f"Ne mogu da se konektujem u voice")
            return
    else:
        voice_client = bot.voice_clients[0]

    await ctx.channel.send(f"{ctx.author.name} je pustio - **{title}**")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            song_info = ydl.extract_info(url, download=False)
    except:
        await ctx.channel.send(f"YouTube zajebava, pokusaj opet")
        return

    if voice_client.is_playing():
        voice_client.stop()

    voice_client.current_url = song_info["url"]
    voice_client.play(discord.FFmpegPCMAudio(song_info["url"]))

@bot.command()
async def s(ctx: Context):
    if bot.voice_clients:
        bot.voice_clients[0].stop()
        await bot.voice_clients[0].disconnect(force=True)
        await ctx.channel.send("https://tenor.com/view/moistcritikal-leaving-meme-gif-23706301")

bot.run(TOKEN)