import discord
from discord import app_commands
from discord.ext import commands
import random

from api import get_media_resources

MEDIA_LINK = "https://unswwit.com/media/"


class RandomResourceCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="random-resource", description="Send a random WIT resource!"
    )
    async def send_random_resource(self, int: discord.Interaction):
        link = ""
        resources = get_media_resources()
        resource_type = random.choice(list(resources.keys()))
        resource = random.choice(resources[resource_type]).fields()
        resource_title = ""

        if resource_type == "publication":
            link = f"{MEDIA_LINK}{resource_type}/{resource['index']}"
            resource_title = resource["heading"]
        elif resource_type == "blog":
            link = f"{MEDIA_LINK}{resource_type}/{resource['index']}"
            resource_title = resource["title"]
        elif resource_type == "podcast":
            link = resource["link"]
            resource_title = resource["title"]

        try:
            message = f"**{resource_type.capitalize()} Recommendation\n**Name: {resource_title}\nLink: {link}"
            await int.response.send_message(message)
        except:
            await int.response.send_message("Sorry, no posts yet!")


async def setup(bot: commands.Bot):
    await bot.add_cog(RandomResourceCog(bot))
