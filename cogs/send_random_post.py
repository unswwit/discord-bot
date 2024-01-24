import discord
from discord import app_commands
from discord.ext import commands

from api import get_random_marketing_post
import io
import aiohttp

from oweek_ctf import run_ctf

class RandomPostCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="random-willow-motivation", description="Send a random motivational post!"
    )
    async def send_random_motivation(self, int: discord.Interaction):
        await send_post(int, get_random_marketing_post("Monday"))

        # Run O-Week CTF
        await run_ctf(int.user)

    @app_commands.command(
        name="random-willow-meme", description="Send a random Willow meme!"
    )
    async def sendRandomMeme(self, int: discord.Interaction):
        await send_post(int, get_random_marketing_post("Memes"))

        # Run O-Week CTF
        await run_ctf(int.user)

    @app_commands.command(
        name="random-willow-post", description="Send a random Willow post!"
    )
    async def sendRandomWillow(self, int: discord.Interaction):
        await send_post(int, get_random_marketing_post("Mascot"))

        # Run O-Week CTF
        await run_ctf(int.user)


async def send_post(int: discord.Interaction, randomPost):
    random_post_fields = randomPost.fields()
    label = random_post_fields.get("label").replace(" ", "-") + ".png"
    link = "https:" + random_post_fields.get("img").url()

    async with aiohttp.ClientSession() as session:
        await int.response.defer()
        async with session.get(link) as resp:
            if resp.status != 200:
                return await int.followup.send("Could not download file...")
            data = io.BytesIO(await resp.read())
            await int.followup.send(file=discord.File(data, label))


async def setup(bot: commands.Bot):
    await bot.add_cog(RandomPostCog(bot))
