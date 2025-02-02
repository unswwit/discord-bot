import discord
from discord import app_commands
from discord.ext import commands
from shapes import shapes_list
import random

class RandomShapeGenerate(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    @app_commands.command(
        name="random-shape", description="Give a random shape!"
    )
    async def send_random_object(self, inter: discord.Interaction):
        random_shape = random.choice(shapes_list)
        await inter.response.send_message(random_shape["name"])
        
async def setup(bot: commands.Bot):
    await bot.add_cog(RandomShapeGenerate(bot))
