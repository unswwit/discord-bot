import discord
from discord import app_commands
from discord.ext import commands
import random_topic

class randomTopicCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    # user types/random_topic and the command will be executed
    @app_commands.command(name="random-topic")
    async def random_topic_command(self, int: discord.Interaction):
        # generates a random topic from random_topic module and saves it to a variable called topic
        topic = random_topic.get_topic()
        # creates a string called message allowing variables to be included
        message = f"**Conversation topic:** {topic}"
        await int.response.send_message(message)


async def setup(bot: commands.Bot):
    await bot.add_cog(randomTopicCog(bot))
