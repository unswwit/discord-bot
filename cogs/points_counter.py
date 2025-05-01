from typing import Optional
import discord
from discord import app_commands
from discord.ext import commands

TEAMS = [
    "Execs", 
    "Careers", 
    "Competitions", 
    "Sponsorships", 
    "HR", 
    "Socials", 
    "Marketing", 
    "Media", 
    "Publications", 
    "Education", 
    "IT"
]


class PointsCounterCog(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        # Initialise storage

    counter = app_commands.Group(
        name="points-counter", 
        description="A scoreboard for 2025 Hogwarts challenges!"
    )

    # Subcommands
    @counter.command(
        name="add", description="Add or remove points"
    )
    @app_commands.describe(portfolio="Choose a port")
    @app_commands.describe(amount="Points to add (negative to subtract)")
    @app_commands.describe(desc="Activity description (optional)")
    # Manage permissions so only admin can?
    async def add_points(
        self, 
        inter: discord.Interaction,
        portfolio: discord.Role,
        amount: int,
        desc: Optional[str]
    ):
        # Load in data - with @role tags 
        # Adjust score
        # Make a record of the action
        # Send response
        pass

    @counter.command(
        name="display", description="Shows all scores"
    )
    # Manage permissions so only admin can?
    async def add_points(self, inter: discord.Interaction):
        # Load data
        # Sort by score descending
        # Label top three with medal emojis 🥇🥈🥉
        # Send response
        pass


async def setup(bot: commands.Bot):
    await bot.add_cog(PointsCounterCog(bot))