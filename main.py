import os
import sys
import discord
import yt_dlp
import aiohttp
import asyncio

from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import Context

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
async def p(ctx: Context, *, arg):
    if not ctx.author.voice:
        await ctx.channel.send("Moras biti u voice kanalu prvo")
        return
    
    loading_msg = await ctx.channel.send("Ucitavam...")
    
    if not bot.voice_clients:
        try:
            voice_client = await ctx.author.voice.channel.connect()
        except:
            await ctx.channel.send(f"Ne mogu da se konektujem u voice")
            return
    else:
        voice_client = bot.voice_clients[0]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            if url := youtube_url_validation(arg):
                url = url.group(0)
                song_info = ydl.extract_info(url, download=False)
            else:
                song_info = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
    except:
        await ctx.channel.send(f"Nesto nije u redu, pokusaj opet")
        return
    
    await loading_msg.delete()
    
    await ctx.channel.send(f"{ctx.author.name} je pustio - **{song_info['title']}**")

    if voice_client.is_playing():
        voice_client.stop()
        await asyncio.sleep(2)

    voice_client.current_url = song_info["url"]
    voice_client.play(discord.FFmpegPCMAudio(song_info["url"]))

@bot.command()
async def s(ctx: Context):
    if bot.voice_clients:
        bot.voice_clients[0].stop()
        await bot.voice_clients[0].disconnect(force=True)
        await ctx.channel.send("https://tenor.com/view/moistcritikal-leaving-meme-gif-23706301")

@bot.command()
async def mmm(ctx: Context):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.waifu.pics/sfw/neko') as resp:
            data = await resp.json()
            await ctx.channel.send(data['url'])

@bot.command()
async def source(ctx: Context):
    if bot.voice_clients:
        if not bot.voice_clients[0].is_playing():
            await ctx.channel.send("Mora nesta svirati prvo")
        else:
            await ctx.channel.send(bot.voice_clients[0].current_url)
    else:
        await ctx.channel.send("Mora nesta svirati prvo")

@bot.command()
async def restart(ctx: Context):
    os.execl(sys.executable, sys.executable, *sys.argv)

bot.run(TOKEN)