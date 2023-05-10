import discord
from discord import app_commands
from discord.ext import commands
import itertools

class helpCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
                    
    @app_commands.command(
        name="help", description="List all commands!"
    )
    async def send_bot_help(self, int: discord.Interaction):
        # TODO: figure out how to parse cogs to show up in /help menu
        embed = discord.Embed(
            title="WillowBot Help", color=0xFEB14B
        ) 
        # TODO: iterate through current cogs to add fields to embed
        # TODO: clean up embed
        embed.set_footer(
                    text="Type /help command for more info on a command (e.g. /help random-willow-meme)")
        await int.response.send_message(embed=embed)
    
    # TODO: add error handling
    # TODO: add individual help commands

async def setup(bot: commands.Bot):
    await bot.add_cog(helpCog(bot))
