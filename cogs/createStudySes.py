import discord
from discord.ext import commands
from discord.ui import Button
from discord import app_commands

class createStudySes(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="create-study-session", description=)
    async def create_study_session(self, ctx: commands.Context, date: str, start_time: str, end_time: str):
        username = ctx.author.name
        message_content = f"Study Session!\n\n{username} is having a study session for {date} from {start_time} to {end_time} in the WIT Discord Server! Click the buttons below to RSVP.\n\nAttendees (1):\n{username}"
        embed = discord.Embed(description=message_content, color=discord.Color.blue())
        await ctx.send(embed=embed)        

class MyView(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(Button(style=discord.ButtonStyle.green, label="Going"))
        self.add_item(Button(style=discord.ButtonStyle.red, label="Not Going"))


class Buttons(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test_buttons(self, ctx):
        view = MyView()
        await ctx.send("Are you going or not?", view=view)


async def setup(bot):
    bot.add_cog(Buttons(bot))
