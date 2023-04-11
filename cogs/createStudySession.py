import discord
from discord.ext import commands
from discord import app_commands
import time
import math


class createStudySessionCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="create-study-session",
        description="Schedule a study session and invite WIT Discord members!",
    )
    @app_commands.describe(
        date="The date of your study session, formatted as YYYY-MM-DD. (e.g. 2023-04-10)",
        start_time="The starting time of your study session, formatted as HH:MM. (e.g. 13:30)",
        end_time="The ending time of your study session, formatted as HH:MM. (e.g. 14:30)",
    )
    async def create_study_session(
        self, inter: discord.Interaction, date: str, start_time: str, end_time: str
    ):
        # Discord timestamp formatting
        startUnix = time.mktime(time.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M"))
        startString = f"<t:{math.floor(startUnix)}:F>"
        endUnix = time.mktime(time.strptime(f"{date} {end_time}", "%Y-%m-%d %H:%M"))
        endString = f"<t:{math.floor(endUnix)}:t>"

        id = inter.user.id
        messageContent = f"""
        **🧡 Study Session! 🧡**\n\n<@{id}> is having a study session on {startString} until {endString} in the WIT Discord Server!\n\nClick the buttons below to RSVP.\n\n
        """
        embed = discord.Embed(
            title=f"Attendees (1):",
            description=f"\n\n- <@{id}>",
            color=discord.Color.orange(),
        )
        view = MyView(id)
        await inter.response.send_message(
            content=messageContent, embed=embed, view=view
        )


class MyView(discord.ui.View):
    def __init__(self, creatorId):
        super().__init__(timeout=None)
        self.attendees = {creatorId}  # initialize set of attendees

    @discord.ui.button(style=discord.ButtonStyle.green, label="Going")
    async def going(self, inter: discord.Interaction, button: discord.ui.Button):
        self.attendees.add(inter.user.id)
        await self.updateMessage(inter)

    @discord.ui.button(style=discord.ButtonStyle.red, label="Not Going")
    async def notGoing(self, inter: discord.Interaction, button: discord.ui.Button):
        self.attendees.discard(inter.user.id)
        await self.updateMessage(inter)

    async def updateMessage(self, inter: discord.Interaction):
        attendeesList = "\n".join(f"- <@{attendee}>" for attendee in self.attendees)

        embed = discord.Embed(
            title=f"Attendees ({len(self.attendees)}):",
            color=discord.Color.orange(),
            description=f"\n\n{attendeesList}",
        )
        await inter.response.edit_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(createStudySessionCog(bot))
