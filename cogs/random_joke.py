import discord
from discord import app_commands
from discord.ext import commands
import requests

link = "https://official-joke-api.appspot.com/jokes/random"


class RandomJokeCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
            name="random-joke", description="Tell a random joke!"
    )
    
    async def send_random_joke(self, inter: discord.Interaction):
        response = requests.get(link)
        if response.status_code == 200:
            data = response.json()
            message = f"**Topic:** {data.get('type').capitalize()}\n**The Joke:** {data.get('setup')}\n**Punchline:** {data.get('punchline')}"
            await inter.response.send_message(message)
        else:
            await inter.response.send_message("Failed to retrieve random joke")


async def setup(bot: commands.Bot):
    await bot.add_cog(RandomJokeCog(bot))
