import discord
from discord import app_commands
from discord.ext import commands

from api import getNextUpcomingEvent, getUpcomingEvents, getMostRecentEvent

EVENT_RECAPS_LINK = 'https://unswwit.com/events/event-recaps/'


class upcomingEventsCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="next-upcoming-event", description="See information about WIT's next upcoming event!")
    async def nextUpcomingEvent(self, int: discord.Interaction):
        try:
            nextEventFields = getNextUpcomingEvent().fields()
            await int.response.send_message(f"**🧡 WIT's next event is *{nextEventFields.get('date')}*! 🧡**\n\n**Event Details:** {nextEventFields.get('title')}\n\n{nextEventFields.get('description')}\n**Event Link: **{nextEventFields.get('facebook_link')}")
        except:
            await noEventsMessage(int)

    @app_commands.command(name="all-upcoming-events", description="See an overview of all of WIT's upcoming events!")
    async def upcomingEvents(self, int: discord.Interaction):
        upcomingEvents = getUpcomingEvents()
        if len(upcomingEvents) == 0:
            return await noEventsMessage(int)

        overview = "**🧡 WIT's Upcoming Events 🧡**"
        for event in upcomingEvents:
            eventFields = event.fields()
            overview += f"\n\n*{eventFields.get('date')}*\n{eventFields.get('title')}: <{eventFields.get('facebook_link')}>"
        await int.response.send_message(overview)


async def noEventsMessage(int: discord.Interaction):
    recentEventFields = getMostRecentEvent().fields()
    return await int.response.send_message(f"Unfortunately WIT has no upcoming events for now! Keep an eye out on our socials for new events every term 🧡\n\n**Most Recent Event**\n{recentEventFields.get('title')}: {EVENT_RECAPS_LINK}{recentEventFields.get('year')}/{recentEventFields.get('event_number')}")


async def setup(bot: commands.Bot):
    await bot.add_cog(upcomingEventsCog(bot))
