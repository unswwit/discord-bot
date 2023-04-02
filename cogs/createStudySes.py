# from discord.ui import Button as UIButton
# import discord
# from discord.ext import commands
# from discord.ui import Button
# from discord import app_commands
# from discord.ext.commands import Context


# class createStudySes(commands.Cog):
#     def __init__(self, bot: commands.Bot):
#         self.bot = bot
#         self.attendees = []  # initialize an empty list of attendees

#     @app_commands.command(name="create-study-session", description="Create a study session with members")
#     async def create_study_session(self, int: discord.Interaction, date: str, start_time: str, end_time: str):
#         username = int.user.name
#         message_content = f"Study Session!\n\n{username} is having a study session for {date} from {start_time} to {end_time} in the WIT Discord Server! Click the buttons below to RSVP.\n\nAttendees ({len(self.attendees)+1}):\n{username}"
#         embed = discord.Embed(description=message_content,
#                               color=discord.Color.blue())
#         view = MyView(self.add_attendee)
#         await int.response.send_message(embed=embed, view=view)

#     def add_attendee(self, user: discord.User):
#         self.attendees.append(user.name)


# class MyView(discord.ui.View):
#     def __init__(self, callback):
#         super().__init__()
#         self.callback = callback

#         self.add_item(Button(style=discord.ButtonStyle.green, label="Going"))
#         # self.add_item(Button(style=discord.ButtonStyle.red, label="Not Going"))

#     @discord.ui.button(label="Not Going", style=discord.ButtonStyle.red)
#     async def not_going_button(self, button: discord.ui.Button, interaction: discord.Interaction):
#         await interaction.response.defer()

#     @discord.ui.button(label="Going", style=discord.ButtonStyle.green, custom_id="going")
#     async def going_button(self, button: discord.ui.Button, interaction: discord.Interaction):
#         await interaction.response.defer()
#         self.callback(interaction.user)


# async def setup(bot: commands.Bot):
#     await bot.add_cog(createStudySes(bot))

# bold text,
# add help text/description of what to enter (date...)
# Enter the date of your study session! (DD/MM/YYY)
# Enter the starting time of your study session! (Xpm)
# Enter the ending time of your study session! (Xpm)

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
        message_content = f"Study Session!\n\n{username} is having a study session for {date} from {start_time} to {end_time} in the WIT Discord Server! Click the buttons below to RSVP.\n\nAttendees ({len(self.attendees) + 1}):\n{username}\n{self.get_attendees_list()}"
        embed = discord.Embed(description=message_content,
                              color=discord.Color.blue())
        view = MyView(self.add_attendee, username)
        await inter.response.send_message(embed=embed, view=view)

    # def remove_attendee(self, user: discord.User):
    #     self.attendees.append(user)
    #     print(f"Added attendee: {', '.join(self.attendees)}")

    def add_attendee(self, user: discord.User):
        self.attendees.append(user.display_name)
        # gets rid of duplicates
        # self.attendees = list(set(self.attendees))

    def get_attendees_list(self):
        attendees_list = "\n".join(
            f"- {attendee.name}" for attendee in self.attendees)
        return attendees_list


class MyView(discord.ui.View):
    def __init__(self, callback, username):
        super().__init__()
        self.callback = callback

        self.add_item(Button(style=discord.ButtonStyle.green,
                      label="Going", custom_id="going"))
        self.add_item(Button(style=discord.ButtonStyle.red,
                      label="Not Going", custom_id="not_going"))

    async def on_button_click(self, button: discord.ui.Button, inter: discord.Interaction):
        await self.callback(inter, button)


# class MyView(discord.ui.View):
#     def __init__(self, callback, username):
#         super().__init__()
#         self.callback = callback
#         self.username = username

#         self.add_item(Button(style=discord.ButtonStyle.green,
#                       label="Going", custom_id="going"))
#         self.add_item(Button(style=discord.ButtonStyle.red,
#                       label="Not Going", custom_id="not_going"))

#     async def on_button_click(self, button: discord.ui.Button, inter: discord.Interaction):
#         if button.custom_id == "going":
#             await self.callback(inter.user, self.username)
#         self.clear_items()
#         self.add_item(Label("Thanks for RSVP'ing!"))


async def setup(bot: commands.Bot):
    await bot.add_cog(createStudySes(bot))
