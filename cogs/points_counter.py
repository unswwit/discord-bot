import discord, os
from typing import Optional
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from pyairtable import Api

load_dotenv()
ACCESS_TOKEN = os.getenv("AIRTABLE_TOKEN")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")
TABLE_ID = os.getenv("AIRTABLE_TABLE_ID")

api = Api(ACCESS_TOKEN)
table = api.table(BASE_ID, TABLE_ID)

records = table.all()

def update_points(team, points):
    try:
        rec = table.first(formula=f"({{Team}} = '{team}')")
        rec_id = rec["id"]
        curr_points = rec["fields"]["Points"]
        new_points = curr_points + points
        table.update(rec_id, {"Points": new_points})
        return True
    except:
        return False


class PointsCounterCog(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    counter = app_commands.Group(
        name="points-counter", description="A scoreboard for the 2025 Hogwarts challenges!"
    )

    # Subcommands
    @counter.command(
        name="add", description="Add or remove points"
    )
    @app_commands.describe(
        team="Choose a team",
        amount="Points to add (negative to subtract)",
        desc="Activity description (optional)"
    )
    # Manage permissions so only admin can?
    async def add_points(
        self, 
        inter: discord.Interaction,
        team: discord.Role,
        amount: int,
        desc: Optional[str]
    ):
        # Load in data - with @role tags 
        # Adjust score in database
        team_name = team.name

        if update_points(team_name, amount):
            # Send response upon update success for user only
            await inter.response.send_message(
                f"Points successfully added for {team_name}!",
                ephemeral=True
            )
        else:
            await inter.response.send_message(
                f"An error occurred trying to update points, please try again.",
                ephemeral=True
            )
        # Make a record of the action [optional for later]

    @counter.command(
        name="display", description="Shows all scores"
    )
    # Manage permissions so only admin can?
    async def show_points(self, inter: discord.Interaction):
        # Load data
        # Sort by score descending
        # Label top three with medal emojis 🥇🥈🥉
        # Send response
        pass


async def setup(bot: commands.Bot):
    await bot.add_cog(PointsCounterCog(bot))
    