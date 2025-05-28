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
LOG_ID = os.getenv("AIRTABLE_LOG_ID")

api = Api(ACCESS_TOKEN)
points_table = api.table(BASE_ID, TABLE_ID)
log_table = api.table(BASE_ID, LOG_ID)


def update_points(team, points):
    try:
        rec = points_table.first(formula=f"({{Team}} = '{team}')")
        rec_id = rec["id"]
        curr_points = rec["fields"]["Points"]
        new_points = curr_points + points
        points_table.update(rec_id, {"Points": new_points})
        return True
    except:
        return False


def display_points():
    team_points = {}
    try:
        points_data = points_table.all()
    except:
        return None

    for r in points_data:
        fields = r["fields"]
        team = fields["Team"]
        points = int(fields.get("Points", 0))
        team_points[team] = int(points)

    out_lines = []
    sorted_list = sorted(team_points.items(), key=lambda x: (-x[1], x[0]))
    for pos, i in enumerate(sorted_list, 1):
        team, points = i
        if pos == 1:
            out_lines.append(f"🥇 1st - **{team}**: {points} points")
        elif pos == 2:
            out_lines.append(f"🥈 2nd - **{team}**: {points} points")
        elif pos == 3:
            out_lines.append(f"🥉 3rd - **{team}**: {points} points")
        else:
            out_lines.append(f"{pos:>8}th - **{team}**: {points} points")

    return out_lines


def display_log():
    out_lines = []
    out_lines.append("**Latest updates**\n")

    try:
        sorted_log = sorted(
            log_table.all(), key=lambda x: x["createdTime"], reverse=True
        )
    except:
        return None
    num_logs = len(sorted_log)
    if num_logs == 0:
        return "No updates to points yet."

    for i in range(0, min(num_logs, 10)):
        r = sorted_log[i]
        createdTime = r["createdTime"][:10].split("-")[::-1]
        createdTime = "-".join(createdTime)
        res = r["fields"].values()
        if len(res) > 1:
            action, desc = res
            out_lines.append(f"{i + 1}. {action} on {createdTime} for: {desc}\n")
        else:
            (action,) = res
            out_lines.append(f"{i + 1}. {action} on {createdTime}\n")
    return "".join(out_lines).strip()


class PointsCounterCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    counter = app_commands.Group(
        name="points-counter",
        description="A scoreboard for the 2025 Hogwarts challenges!",
    )

    # Subcommands
    @counter.command(name="add", description="Add or remove points")
    @app_commands.describe(
        team="Choose a team",
        amount="Points to add (negative to subtract)",
        desc="Activity description (optional)",
    )
    async def add_points(
        self,
        inter: discord.Interaction,
        team: discord.Role,
        amount: int,
        desc: Optional[str] = None,
    ):
        # Checking that only admin is running command
        if not inter.user.guild_permissions.administrator:
            await inter.response.send_message(
                "❌ You must be an admin to add points to teams.", ephemeral=True
            )
            return

        # Adjust score in database
        team_name = team.name
        if update_points(team_name, amount):
            # Send response upon update success for user only
            await inter.response.send_message(
                f"Points successfully added for {team_name}!", ephemeral=True
            )

            # Make a record of the action in points log
            action = f"+{amount} {team_name}"
            log = {"Action": action}
            if desc:
                log["Description"] = desc
            log_table.create(log)
        else:
            await inter.response.send_message(
                f"An error occurred trying to update points, please try again.",
                ephemeral=True,
            )

    @counter.command(name="display", description="Shows all scores")
    async def show_points(self, inter: discord.Interaction):
        res = display_points()
        if res:
            await inter.response.send_message("\n".join(res))
        else:
            await inter.response.send_message(
                f"An error occurred trying to display points, please try again.",
                ephemeral=True,
            )

    @counter.command(name="log", description="Shows all changes to points")
    async def show_log(self, inter: discord.Interaction):
        res = display_log()
        if res:
            await inter.response.send_message(res, ephemeral=True)
        else:
            await inter.response.send_message(
                f"An error occurred trying to display log, please try again.",
                ephemeral=True,
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(PointsCounterCog(bot))
