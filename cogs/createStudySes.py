from discord.ui import Button as UIButton
import discord
from discord.ext import commands
from discord.ui import Button
from discord import app_commands
from discord.ext.commands import Context


class createStudySes(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.attendees = []  # initialize an empty list of attendees

    @app_commands.command(name="create-study-session", description="Create a study session with members")
    async def create_study_session(self, inter: discord.Interaction, date: str, start_time: str, end_time: str):
        username = inter.user.name
        message_content = f"**Study Session!\n\n{username}** is having a study session for **{date} from {start_time} to {end_time}** in the WIT Discord Server! Click the buttons below to RSVP.\n\n**Attendees ({len(self.attendees) + 1}):**\n{username}\n{self.get_attendees_list()}"
        embed = discord.Embed(description=message_content,
                              color=discord.Color.blue())
        view = MyView(self.add_attendee, username)
        await inter.response.send_message(embed=embed, view=view)

    async def add_attendee(self, inter: discord.Interaction, user: discord.User):
        self.attendees.append(user.display_name)
        await inter.response.send_message(f"{user.display_name} has RSVP'd to the study session!")

    def get_attendees_list(self):
        attendees_list = "\n".join(
            f"- {attendee.name}" for attendee in self.attendees)
        return attendees_list


class MyView(discord.ui.View):
    def __init__(self, callback, username):
        super().__init__()
        self.callback = callback
        self.going_users = []  # initialize an empty list for going users
        self.attendees_list = discord.ui.Button(label="Attendees", disabled=True)


    @discord.ui.button(style=discord.ButtonStyle.green, label="Going")
    async def going(self,  inter: discord.Interaction, button: discord.ui.Button):
        await self.callback(inter, inter.user)

    @discord.ui.button(style=discord.ButtonStyle.red, label="Not Going")
    async def not_going(self,  inter: discord.Interaction, button: discord.ui.Button):
        await self.callback(inter, inter.user)

        going_usernames = [f"<@{user_id}>" for user_id in self.going_users]
        self.attendees_list.label = "\n".join(going_usernames)

async def setup(bot: commands.Bot):
    await bot.add_cog(createStudySes(bot))