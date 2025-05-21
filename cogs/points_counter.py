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

def display_points():
    team_points = {}
    for r in table.all():
        team, points = r["fields"].values()
        team_points[team] = int(points)

    out_lines = []
    sorted_list = sorted(team_points.items(), key=lambda x: (-x[1], x[0]))
    for pos, i in enumerate(sorted_list, 1):
        team, points = i
        if pos == 1:
            out_lines.append(f"🥇 1st - {team}: {points} points")
        elif pos == 2:
            out_lines.append(f"🥈 2nd - {team}: {points} points")
        elif pos == 3:
            out_lines.append(f"🥉 3rd - {team}: {points} points")
        else:
            out_lines.append(f"{pos:>4}th - {team}: {points} points")
    
    return out_lines


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
    async def show_points(self, inter: discord.Interaction):
        res = display_points()
        if res:
            await inter.response.send_message('\n'.join(res), ephemeral=True)
        else:
            await inter.response.send_message(
                f"An error occurred trying to display points, please try again.",
                ephemeral=True
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(PointsCounterCog(bot))
