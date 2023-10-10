import discord
import math
import random
from discord.ext import commands
from discord import app_commands

# 24 game
# /24 to play game
# Give us 4 random numbers that can make 24
# Numpad (4x3) of only those 4 numbers, + arithmetic, brackets, equals
# Clicking equals runs solver command to see if statement makes 24
# Correct window
# Incorrect windowx

# Print random numbers that can be used to create 24
arrays_24 = [
    [1, 2, 3, 4],
    [1, 2, 3, 5],
    [1, 2, 3, 6],
    [1, 2, 3, 7],
    [1, 2, 3, 8],
    [1, 2, 3, 9],
    [1, 2, 4, 5],
    [1, 2, 4, 6],
    [1, 2, 4, 7],
    [1, 2, 4, 8],
    [1, 2, 4, 9],
    [1, 2, 5, 6],
    [1, 2, 5, 7],
    [1, 2, 5, 8],
    [1, 2, 5, 9],
    [1, 2, 6, 7],
    [1, 2, 6, 8],
    [1, 2, 6, 9],
    [1, 2, 7, 9],
    [1, 2, 8, 9],
    [1, 3, 4, 5],
    [1, 3, 4, 6],
    [1, 3, 4, 7],
    [1, 3, 4, 8],
    [1, 3, 4, 9],
    [1, 3, 5, 6],
    [1, 3, 5, 7],
    [1, 3, 5, 8],
    [1, 3, 5, 9],
    [1, 3, 6, 9],
    [1, 3, 7, 8],
    [1, 3, 7, 9],
    [1, 3, 8, 9],
    [1, 4, 5, 6],
    [1, 4, 5, 7],
    [1, 4, 5, 8],
    [1, 4, 5, 9],
    [1, 4, 6, 7],
    [1, 4, 6, 8],
    [1, 4, 6, 9],
    [1, 4, 7, 8],
    [1, 4, 7, 9],
    [1, 4, 8, 9],
    [1, 5, 6, 7],
    [1, 5, 6, 8],
    [1, 5, 6, 9],
    [1, 5, 7, 8],
    [1, 5, 7, 9],
    [1, 5, 8, 9],
    [1, 6, 7, 9],
    [1, 6, 8, 9],
    [1, 7, 8, 9],
    [2, 3, 4, 5],
    [2, 3, 4, 6],
    [2, 3, 4, 7],
    [2, 3, 4, 8],
    [2, 3, 4, 9],
    [2, 3, 5, 6],
    [2, 3, 5, 7],
    [2, 3, 5, 8],
    [2, 3, 5, 9],
    [2, 3, 6, 7],
    [2, 3, 6, 8],
    [2, 3, 6, 9],
    [2, 3, 7, 8],
    [2, 3, 7, 9],
    [2, 4, 5, 6],
    [2, 4, 5, 7],
    [2, 4, 5, 8],
    [2, 4, 5, 9],
    [2, 4, 6, 7],
    [2, 4, 6, 8],
    [2, 4, 6, 9],
    [2, 4, 7, 8],
    [2, 4, 7, 9],
    [2, 4, 8, 9],
    [2, 5, 6, 7],
    [2, 5, 6, 8],
    [2, 5, 6, 9],
    [2, 5, 7, 8],
    [2, 5, 7, 9],
    [2, 5, 8, 9],
    [2, 6, 7, 8],
    [2, 6, 7, 9],
    [2, 6, 8, 9],
    [2, 7, 8, 9],
    [3, 4, 5, 6],
    [3, 4, 5, 7],
    [3, 4, 5, 8],
    [3, 4, 5, 9],
    [3, 4, 6, 8],
    [3, 4, 6, 9],
    [3, 4, 7, 8],
    [3, 4, 7, 9],
    [3, 4, 8, 9],
    [3, 5, 6, 7],
    [3, 5, 6, 8],
    [3, 5, 6, 9],
    [3, 5, 7, 8],
    [3, 5, 7, 9],
    [3, 5, 8, 9],
    [3, 6, 7, 8],
    [3, 6, 7, 9],
    [3, 6, 8, 9],
    [3, 7, 8, 9],
    [4, 5, 6, 7],
    [4, 5, 6, 8],
    [4, 5, 6, 9],
    [4, 5, 7, 8],
    [4, 5, 7, 9],
    [4, 6, 7, 8],
    [4, 6, 7, 9],
    [4, 6, 8, 9],
    [4, 7, 8, 9],
    [5, 6, 7, 8],
    [5, 6, 7, 9],
    [5, 6, 8, 9],
    [6, 7, 8, 9],
]


class TwentyFourCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="24", description="Play a game of 24")
    async def play_24(
        self,
        inter: discord.Interaction,
    ):
        await inter.response.defer()


class MyView(discord.ui.View):
    def __init__(self, creator_id):
        super().__init__(timeout=None)
        self.creator_id = creator_id
        random_combination = random.choice(arrays_24)
        self.num1 = random_combination[0]
        self.num2 = random_combination[1]
        self.num3 = random_combination[2]
        self.num4 = random_combination[3]

    async def update_message(self, interaction):
        embed = discord.Embed(title="24", color=discord.Color.orange())
        embed.add_field(
            name="Numbers",
            value=f"`{self.num1}` `{self.num2}` `{self.num3}` `{self.num4}`",
            inline=False,
        )

        await interaction.send(embed=embed)


# async def callback(self, interaction: discord.Interaction):

# async def updateMessageIncorrect(self, interaction: discord.Interaction):

# async def updateMessageCorrect(self, interaction: discord.Interaction):


async def setup(bot: commands.Bot):
    await bot.add_cog(TwentyFourCog(bot))
