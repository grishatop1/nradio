import os
import io
import discord
import asyncio

from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import Context
from pytube import YouTube

from utils import youtube_url_validation


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

    voice_client = await ctx.author.voice.channel.connect()
    
    await ctx.channel.send(f"{ctx.author.name} je pustio - **{title}**")
        

bot.run(TOKEN)