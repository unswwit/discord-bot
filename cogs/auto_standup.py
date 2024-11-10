import discord
import asyncio
import datetime
from datetime import timezone
from discord import app_commands
from discord.ext import commands

channel_ID = 1172727647382552737
day_seconds = 86400
timezone_offset = 11
thursday = 3
hour = 9


class AutoStandups(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.channel_id = channel_ID
        self.time_offset = datetime.timedelta(hours=timezone_offset)
        self.bot.loop.create_task(self.send_weekly_message())

    async def send_weekly_message(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(self.channel_id)
        while not self.bot.is_closed():
            utc_time = datetime.datetime.now(timezone.utc)
            curr_time = utc_time + self.time_offset

            if curr_time.weekday() == thursday and curr_time.hour == hour:
                await channel.send("@IT reminder for standups")
                await asyncio.sleep(day_seconds)
            else:
                days_until_thursday = (thursday - curr_time.weekday()) % 7
                next_thursday = curr_time + datetime.timedelta(days=days_until_thursday)
                next_thursday = next_thursday.replace(
                    hour=hour, minute=0, second=0, microsecond=0
                )
                if next_thursday < curr_time:
                    next_thursday += datetime.timedelta(weeks=1)
                seconds_until_thursday = (next_thursday - curr_time).total_seconds()
                await asyncio.sleep(seconds_until_thursday)


async def setup(bot: commands.Bot):
    await bot.add_cog(AutoStandups(bot))
