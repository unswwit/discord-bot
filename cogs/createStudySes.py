import discord
from discord.ext import commands
from discord.ui import Button
from discord import app_commands
from discord.ext.commands import Context

class createStudySes(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="create-study-session", description="Create a study session with members")
    async def create_study_session(self, int: discord.Interaction, date: str, start_time: str, end_time: str):
        username = int.user.name
        message_content = f"Study Session!\n\n{username} is having a study session for {date} from {start_time} to {end_time} in the WIT Discord Server! Click the buttons below to RSVP.\n\nAttendees (1):\n{username}"
        embed = discord.Embed(description=message_content, color=discord.Color.blue())
        view = MyView()
        await int.response.send_message(embed=embed, view=view)


class MyView(discord.ui.View):
    def __init__(self, author_id):
        super().__init__()
        self.going_users = set([author_id])

        self.add_item(Button(style=discord.ButtonStyle.green, label="Going", custom_id="going"))
        self.add_item(Button(style=discord.ButtonStyle.red, label="Not Going", custom_id="not_going"))
        self.author_id = author_id 

        self.attendees_label = discord.utils.get(self.children, id="attendees_label")
        #this allows the the bot to know which button was clicked so it can respond appropriately 
        if not self.attendees_label:
            self.attendees_label = discord.ui.Button(label="Attendees:", disabled=True, id="attendees_label")
            self.add_item(self.attendees_label)
        
        self.attendees_list = discord.utils.get(self.children, id="attendees_list")
        if not self.attendees_list:
            self.attendees_list = discord.ui.Button(label="", disabled=True, id="attendees_list")
            self.add_item(self.attendees_list)

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id == self.author_id:
            return True
        await interaction.response.send_message("Only the command author can interact with this message.", ephemeral=True)
        return False

    async def on_button_click(self, button: discord.ui.Button, interaction: discord.Interaction):
        if button.custom_id == "going":
            self.going_users.add(interaction.user.id)
        elif button.custom_id == "not_going":
            if interaction.user.id in self.going_users:
                self.going_users.remove(interaction.user.id)

        going_usernames = [f"<@{user_id}>" for user_id in self.going_users]
        self.attendees_list.label = "\n".join(going_usernames)

async def setup(bot: commands.Bot):
    await bot.add_cog(createStudySes(bot))

    @commands.command()
    async def test_buttons(self, ctx):
        view = MyView(ctx.author.id)
        await ctx.send("Are you going or not?", view=view) 


async def setup(bot):
    bot.add_cog(Buttons(bot))

# bold text, 
# add help text/description of what to enter (date...)
# Enter the date of your study session! (DD/MM/YYY)
# Enter the starting time of your study session! (Xpm)
# Enter the ending time of your study session! (Xpm)