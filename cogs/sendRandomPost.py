import discord
from discord.ext import commands

from api import getRandomMarketingPost
import io
import aiohttp


class sendRandomPostCog(commands.Cog, name="Send random post commands"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="random-willow-motivation", help="Send a random motivational post!")
    async def sendRandomMotivation(self, int: discord.Interaction):
        await sendPost(int, getRandomMarketingPost('Monday'))

    @commands.command(name="random-willow-meme", help="Send a random willow meme!")
    async def sendRandomMeme(self, int: discord.Interaction):
        await sendPost(int, getRandomMarketingPost('Memes'))

    @commands.command(name="random-willow-post", help="Send a random willow post!")
    async def sendRandomWillow(self, int: discord.Interaction):
        await sendPost(int, getRandomMarketingPost('Mascot'))


async def sendPost(int: discord.Interaction, randomPost):
    async with aiohttp.ClientSession() as session:
        await int.response.defer()
        async with session.get(randomPost.get('link')) as resp:
            if resp.status != 200:
                return await int.followup.send('Could not download file...')
            data = io.BytesIO(await resp.read())
            await int.followup.send(file=discord.File(data, randomPost.get('label')))


async def setup(bot: commands.Bot):
    await bot.add_cog(sendRandomPostCog(bot))
