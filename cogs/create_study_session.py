import discord
from discord.ext import commands
from discord import app_commands
import math
import datetime as dt
from zoneinfo import ZoneInfo

from oweek_ctf import run_ctf

class CreateStudySessionCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="create-study-session",
        description="Schedule a study session and invite WIT Discord members!",
    )
    @app_commands.describe(
        date="The date of your study session, formatted as YYYY-MM-DD. (e.g. 2023-04-10)",
        start_time="The starting time of your study session in Sydney time, formatted as HH:MM. (e.g. 13:30)",
        end_time="The ending time of your study session in Sydney time, formatted as HH:MM. (e.g. 14:30)",
    )
    async def create_study_session(
        self, inter: discord.Interaction, date: str, start_time: str, end_time: str
    ):
        timezone = ZoneInfo("Australia/Sydney")
        date_format = "%Y-%m-%d %H:%M"
        try:
            start_time = dt.datetime.strptime(
                f"{date} {start_time}", date_format
            ).replace(tzinfo=timezone)
            end_time = dt.datetime.strptime(f"{date} {end_time}", date_format).replace(
                tzinfo=timezone
            )
        except ValueError:
            # send ephemeral error message for incorrect input formatting
            await inter.response.send_message(
                f"**Error: Invalid input format!**\nI couldn't schedule your study session because of some incorrect formatting. See below for details:\n\n**Correct formats:**\ndate: YYYY-MM-DD\nstart_time: HH:MM in Sydney time\nend_time: HH:MM in Sydney time\n\n**You entered:**\ndate: {date}\nstart_time: {start_time}\nend_time: {end_time}",
                ephemeral=True,
            )
            return

        # Discord timestamp formatting
        start_string = f"<t:{math.floor(start_time.timestamp())}:F>"
        end_string = f"<t:{math.floor(end_time.timestamp())}:t>"

        id = inter.user.id

        message_content = f"""
        **🧡 Study Session! 🧡**\n\n<@{id}> is having a study session on {start_string} until {end_string} in the WIT Discord Server!\n\nClick the buttons below to RSVP.\n\n
        """
        embed = discord.Embed(
            title=f"Attendees (1):",
            description=f"\n\n- <@{id}>",
            color=discord.Color.orange(),
        )
        view = MyView(id)
        await inter.response.send_message(
            content=message_content,
            embed=embed,
            view=view,
        )

        # Run O-Week CTF
        await run_ctf(inter.user)


class MyView(discord.ui.View):
    def __init__(self, creator_id):
        super().__init__(timeout=None)
        self.attendees = {creator_id}  # initialize set of attendees

    @discord.ui.button(style=discord.ButtonStyle.green, label="Going")
    async def going(self, inter: discord.Interaction, button: discord.ui.Button):
        self.attendees.add(inter.user.id)
        await self.update_message(inter)

    @discord.ui.button(style=discord.ButtonStyle.red, label="Not Going")
    async def not_going(self, inter: discord.Interaction, button: discord.ui.Button):
        self.attendees.discard(inter.user.id)
        await self.update_message(inter)

    async def update_message(self, inter: discord.Interaction):
        attendees_list = "\n".join(f"- <@{attendee}>" for attendee in self.attendees)

        embed = discord.Embed(
            title=f"Attendees ({len(self.attendees)}):",
            color=discord.Color.orange(),
            description=f"\n\n{attendees_list}",
        )
        await inter.response.edit_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(CreateStudySessionCog(bot))
