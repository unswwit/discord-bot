import discord 
import math
import random 
from discord.ext import commands
from discord import app_commands

class TwentyFourCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="24", description="Play a game of 24!")
    async def play24(
        self,
        inter: discord.Interaction,
    ):
        await inter.response.defer()

