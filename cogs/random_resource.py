import discord
from discord import app_commands
from discord.ext import commands
import random

from api import get_random_resource

class RandomResourceCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="random-resource", description="Send a random WIT resource!"
    )

    async def send_random_resource(self, int: discord.Interaction):
        link_format = "https://unswwit.com/media/"
        link = ""
        resources = get_random_resource()
        resource_type = random.choice(list(resources.keys()))
        resource = None
        resource_title = ""

        if resource_type == "publication":
            resource = random.choice(resources[resource_type]).fields()
            link = f"{link_format}{resource_type}/{resource['index']}"
            resource_title = resource["heading"]
        elif resource_type == "blog":
            resource = random.choice(resources[resource_type]).fields()
            link = f"{link_format}{resource_type}/{resource['index']}"
            resource_title = resource["title"]
        elif resource_type == "podcast":
            resource = random.choice(resources[resource_type]).fields()
            link = resource["link"]
            resource_title = resource["title"]
        
        print(resource)

        message = f"**{resource_type.capitalize()} Recommendation\n**Name: {resource_title}\nLink: {link}"
        await int.response.send_message(message)
       # except:
          
          #  await int.response.send_message("Sorry, no posts yet!")


async def setup(bot: commands.Bot):
    await bot.add_cog(RandomResourceCog(bot))

