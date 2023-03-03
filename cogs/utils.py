import discord
from discord.ext import commands

class helpCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.help_command = sendHelpCommand()


class sendHelpCommand(commands.HelpCommand):
    async def send_error_message(self, error):
        embed = discord.Embed(title="Error", description=error)
        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_bot_help(self, mapping):
        embed = discord.Embed(
            title="Help Command", color=0xFEB14B
        )
        for cog, commands in mapping.items():
            # skip commands not in a cog/category
            if cog is None:
                continue
            filtered = await self.filter_commands(commands, sort=True)
            command_signatures = [
                self.get_command_signature(c) for c in filtered]
            if command_signatures:
                cog_name = getattr(cog, "qualified_name", "No Category")
                embed.add_field(name=cog_name, value="\n".join(
                    command_signatures), inline=False)
                embed.set_footer(
                    text="Type /help command for more info on a command.")
        channel = self.get_destination()
        await channel.send(embed=embed)


async def setup(bot):
    bot.remove_command('help')
    await bot.add_cog(helpCog(bot))
