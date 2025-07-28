from typing import Optional
import zoneinfo
import discord
import asyncio
import datetime
from discord import app_commands
from discord.ext import commands

CHANNEL_ID = 1350004137873637396
DAY_SECONDS = 86400
AUS_SYDNEY_TIMEZONE = zoneinfo.ZoneInfo("Australia/Sydney")


class AutoStandups(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.channel_id = CHANNEL_ID
        self.day = 4  # Friday by default
        self.hour = 10  # 10AM by default
        self.suffix = "AM"
        self.msg = "@Information Technology (IT) reminder to post standups ⭐"
        self.weekly_reminder = None

    @app_commands.command(name="set-standup", description="Set auto-standups in current channel or change details of current ones")
    @app_commands.describe(
        day="Choose a day to set a standup reminder",
        hour="Choose the hour [1-12]",
        suffix="AM or PM",
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
        ],
        suffix=[
            app_commands.Choice(name="AM", value="AM"),
            app_commands.Choice(name="PM", value="PM"),
        ]
    )
    async def set_standup(
        self,
        inter: discord.Interaction,
        day: app_commands.Choice[int],
        hour: int,
        suffix: app_commands.Choice[str],
        msg: Optional[str] = None,
    ):
        self.channel_id = inter.channel_id
        self.day = day.value
        self.suffix = suffix.value

        if hour >= 1 and hour <= 12:
            self.hour = hour
        else:
            await inter.response.send_message(
                f"Please choose an hour between 1 and 12", ephemeral=True
            )
            return

        if msg:
            self.msg = msg

        # Ensuring only one reminder is active
        if self.weekly_reminder is None or self.weekly_reminder.done():
            self.weekly_reminder = self.bot.loop.create_task(self.send_weekly_message())
            await inter.response.send_message(f"Auto-standup successfully set for {day.name} at {self.hour}:00 {suffix.name}\nMessage: {self.msg}", ephemeral=True)
        else:
            await inter.response.send_message(f"There is currently an active auto-standup for {day.name} at {self.hour}:00 {suffix.name}\nMessage: {self.msg}", ephemeral=True)

        return

    async def send_weekly_message(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(self.channel_id)

        try:
            while not self.bot.is_closed():
                curr_time = datetime.datetime.now(AUS_SYDNEY_TIMEZONE)

                target_hour = (self.hour % 12) + (12 if self.suffix == "PM" else 0)

                if curr_time.weekday() == self.day and curr_time.hour == target_hour:
                    await channel.send(self.msg)
                    await asyncio.sleep(DAY_SECONDS)
                else:
                    days_until_next = (self.day - curr_time.weekday()) % 7
                    next_day = curr_time + datetime.timedelta(days=days_until_next)
                    next_day = next_day.replace(
                        hour=target_hour, minute=0, second=0, microsecond=0
                    )
                    if next_day < curr_time:
                        next_day += datetime.timedelta(weeks=1)
                    seconds_until_next = (next_day - curr_time).total_seconds()
                    await asyncio.sleep(seconds_until_next)
        except asyncio.CancelledError:
            return

    @app_commands.command(name="stop-standup", description="Cancel the current standup reminders")
    async def stop_standup(
        self,
        inter: discord.Interaction
    ):
        if self.weekly_reminder and not self.weekly_reminder.done():
            self.weekly_reminder.cancel()
            await inter.response.send_message("🚫 The current standup reminders have been cancelled.", ephemeral=True)
        else:
            await inter.response.send_message("❗There are currently no standup reminders.", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(AutoStandups(bot))
