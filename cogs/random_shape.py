import discord
from discord import app_commands
from discord.ext import commands
# from shapes import shapes_list
from gen_shape import generate_random_shape
import random

class RandomShapeGenerate(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    @app_commands.command(
        name="random-shape", description="Give a random shape!"
    )
    async def send_random_object(self, inter: discord.Interaction):
        # random_shape = random.choice(shapes_list)
        # await inter.response.send_message(random_shape["name"])
        
        # Generate the random shape and save it as a file
        generate_random_shape()

        # Open the saved image to send it to Discord
        with open("random_shape.png", "rb") as f:
            image = discord.File(f, filename="random_shape.png")

        # Send the image as a message
        await inter.response.send_message("Here's a random shape for you!", file=image)

        
async def setup(bot: commands.Bot):
    await bot.add_cog(RandomShapeGenerate(bot))
