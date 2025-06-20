from typing import Optional
import zoneinfo
import discord
import asyncio
import datetime
from datetime import timezone
from discord import app_commands
from discord.ext import commands

CHANNEL_ID = 1350004137873637396
DAY_SECONDS = 86400
AUS_SYDNEY_TIMEZONE = zoneinfo.ZoneInfo("Australia/Sydney")


class AutoStandups(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.channel_id = CHANNEL_ID
        self.bot.loop.create_task(self.send_weekly_message())
        self.day = 4  # Friday by default
        self.hour = 10  # 10AM by default
        self.msg = "@IT reminder to post standups ⭐"

    @app_commands.command(name="set-standup", description="Set up auto-standups")
    @app_commands.describe(
        day="Choose a day to set a standup reminder",
        hour="Choose the hour [0-23]",
        msg="Custom message (optional)",
    )
    @app_commands.choices(
        day=[
            app_commands.Choice(name="Monday", value=0),
            app_commands.Choice(name="Tuesday", value=1),
            app_commands.Choice(name="Wednesday", value=2),
            app_commands.Choice(name="Thursday", value=3),
            app_commands.Choice(name="Friday", value=4),
            app_commands.Choice(name="Saturday", value=5),
            app_commands.Choice(name="Sunday", value=6),
        ]
    )
    async def set_standup(
        self,
        inter: discord.Interaction,
        day: app_commands.Choice[int],
        hour: int,
        msg: Optional[str] = None,
    ):
        self.channel_id = inter.channel_id
        self.day = day.value

        if hour >= 0 and hour <= 23:
            self.hour = hour
        else:
            await inter.response.send_message(
                f"Please choose an hour between 0 and 23", ephemeral=True
            )
            return

        if msg:
            self.msg = msg

        await inter.response.send_message(
            f"Auto-standup successfully set for {day.name} at {hour}:00\nMessage: {self.msg}",
            ephemeral=True,
        )
        return

    async def send_weekly_message(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(self.channel_id)
        while not self.bot.is_closed():
            curr_time = datetime.datetime.now(AUS_SYDNEY_TIMEZONE)

            if curr_time.weekday() == self.day and curr_time.hour == self.hour:
                await channel.send(self.msg)
                await asyncio.sleep(DAY_SECONDS)
            else:
                days_until_next = (self.day - curr_time.weekday()) % 7
                next_day = curr_time + datetime.timedelta(days=days_until_next)
                next_day = next_day.replace(
                    hour=self.hour, minute=0, second=0, microsecond=0
                )
                if next_day < curr_time:
                    next_day += datetime.timedelta(weeks=1)
                seconds_until_next = (next_day - curr_time).total_seconds()
                await asyncio.sleep(seconds_until_next)


async def setup(bot: commands.Bot):
    await bot.add_cog(AutoStandups(bot))
