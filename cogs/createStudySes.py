import discord
from discord.ext import commands
from discord.ui import Button


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


def setup(bot):
    bot.add_cog(Buttons(bot))
