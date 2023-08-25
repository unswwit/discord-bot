import os

import discord
from discord.ext import commands
from discord.ext.commands import Greedy, Context
from dotenv import load_dotenv
from cogwatch import Watcher

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
BOT_NAME = os.getenv("DISCORD_BOT_NAME")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def setup_hook():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"{filename} has loaded!")


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")

    watcher = Watcher(bot, path="cogs", preload=True)  # hot reloading for cogs
    await watcher.start()


@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(ctx: Context, guilds: Greedy[discord.Object], bot_name):
    if not guilds and bot_name == BOT_NAME:
        print("Syncing command(s)...")
        synced = await bot.tree.sync()
        await ctx.send(f"Synced {len(synced)} command(s) globally!")
        return

    await ctx.send(f"Error: tree was not synced.")


bot.run(TOKEN)
