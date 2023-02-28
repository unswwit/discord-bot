import discord
from discord.ext import commands


class helpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        help_command = sendHelpCommand()
        help_command.cog = self
        bot.help_command = help_command

class sendHelpCommand(commands.MinimalHelpCommand):
    async def send_error_message(self, error):
        embed = discord.Embed(title="Error", description=error)
        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_bot_help(self, mapping):
        embed = discord.Embed(
            title="Help Command", description="Type `/help command` for more info on a command.\nYou can also type `/help category` for more info on a category.", color=0xFEB14B
        )
        for cog, commands in mapping.items():
            filtered = await self.filter_commands(commands, sort=True)
            command_signatures = [
                self.get_command_signature(c) for c in filtered]
            if command_signatures:
                cog_name = getattr(cog, "qualified_name", "No Category")
                embed.add_field(name=cog_name, value="\n".join(
                    command_signatures), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

# TODO: implement pagination when we get more commands
# TODO: figure out how to remove duplicate help command

async def setup(bot):
    await bot.add_cog(helpCog(bot))
