import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def setup_hook():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f'cogs.{filename[:-3]}')
            print(f'{filename} has loaded!')

    print(f'{bot.user} has connected to Discord!')

bot.run(TOKEN)
