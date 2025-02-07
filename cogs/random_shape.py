import discord
from discord import app_commands
from discord.ext import commands

from gen_shape import generate_random_shape


class RandomShapeGenerate(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="random-shape", description="Give a random shape!")
    async def send_random_object(self, inter: discord.Interaction):

        # Generate the random shape
        await generate_random_shape(inter.user)

        # Send a message with the shape directly in the same channel
        with open("random_shape.png", "rb") as file:
            await inter.response.send_message(
                f"A random shape has been generated.",
                file=discord.File(file, filename="random_shape.png"),
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(RandomShapeGenerate(bot))
