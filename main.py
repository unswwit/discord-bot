import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from api import getRandomMarketingPost
import io
import aiohttp

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = os.getenv('TEST_GUILD_ID')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    try:
        print("Syncing command(s)...")
        synced = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
        print(f'Synced {len(synced)} command(s)!')
    except Exception as e:
        print(e)
    print(f'{bot.user} has connected to Discord!')


@bot.tree.command(guild=discord.Object(id=GUILD_ID), name="random-willow-motivation", description="Send a random motivational post!")
async def sendRandomMotivation(int: discord.Interaction):
    await sendPost(int, getRandomMarketingPost('Monday'))


@bot.tree.command(guild=discord.Object(id=GUILD_ID), name="random-willow-meme", description="Send a random willow meme!")
async def sendRandomMeme(int: discord.Interaction):
    await sendPost(int, getRandomMarketingPost('Memes'))


@bot.tree.command(guild=discord.Object(id=GUILD_ID), name="random-willow-post", description="Send a random willow post!")
async def sendRandomWillow(int: discord.Interaction):
    await sendPost(int, getRandomMarketingPost('Mascot'))


async def sendPost(int: discord.Interaction, randomPost):
    async with aiohttp.ClientSession() as session:
        await int.response.defer()
        async with session.get(randomPost.get('link')) as resp:
            if resp.status != 200:
                return await int.followup.send('Could not download file...')
            data = io.BytesIO(await resp.read())
            await int.followup.send(file=discord.File(data, randomPost.get('label')))

bot.run(TOKEN)
