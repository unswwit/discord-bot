import discord
from discord import app_commands
from discord.ext import commands

from api import get_next_upcoming_event, get_upcoming_events, get_most_recent_event

from oweek_ctf import run_ctf

EVENT_RECAPS_LINK = "https://unswwit.com/events/event-recaps/"


class UpcomingEventsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="next-upcoming-event",
        description="See information about WIT's next upcoming event!",
    )
    async def next_upcoming_event(self, inter: discord.Interaction):
        try:
            next_event_fields = get_next_upcoming_event().fields()
            await inter.response.send_message(
                f"**🧡 WIT's next event is *{next_event_fields.get('date')}*! 🧡**\n\n**Event Details:** {next_event_fields.get('title')}\n\n{next_event_fields.get('description')}\n**Event Link: **{next_event_fields.get('facebook_link')}"
            )
        except:
            await no_events_message(inter)

        # Run O-Week CTF
        await run_ctf(inter.user)

    @app_commands.command(
        name="all-upcoming-events",
        description="See an overview of all of WIT's upcoming events!",
    )
    async def upcoming_events(self, inter: discord.Interaction):
        upcoming_events = get_upcoming_events()
        if len(upcoming_events) == 0:
            return await no_events_message(inter)

        overview = "**🧡 WIT's Upcoming Events 🧡**"
        for event in upcoming_events:
            event_fields = event.fields()
            overview += f"\n\n*{event_fields.get('date')}*\n{event_fields.get('title')}: <{event_fields.get('facebook_link')}>"
        await inter.response.send_message(overview)

        # Run O-Week CTF
        # await run_ctf(inter.user)


async def no_events_message(int: discord.Interaction):
    recent_event_fields = get_most_recent_event().fields()
    return await int.response.send_message(
        f"Unfortunately WIT has no upcoming events for now! Keep an eye out on our socials for new events every term 🧡\n\n**Most Recent Event**\n{recent_event_fields.get('title')}: {EVENT_RECAPS_LINK}{recent_event_fields.get('year')}/{recent_event_fields.get('event_number')}"
    )


async def setup(bot: commands.Bot):
    await bot.add_cog(UpcomingEventsCog(bot))
