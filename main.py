import os

import discord
from discord.ext import commands
from discord.ext.commands import Greedy, Context
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
BOT_NAME = os.getenv('DISCORD_BOT_NAME')

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def setup_hook():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f'cogs.{filename[:-3]}')
            print(f'{filename} has loaded!')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command()
@commands.guild_only()
@commands.has_permissions(administrator=True)
async def sync(
        ctx: Context, guilds: Greedy[discord.Object], botName):
    if not guilds and botName == BOT_NAME:
        print("Syncing command(s)...")
        synced = await bot.tree.sync()
        await ctx.send(
            f'Synced {len(synced)} command(s) globally!'
        )
        return

    await ctx.send(f"Error: tree was not synced.")

bot.run(TOKEN)
