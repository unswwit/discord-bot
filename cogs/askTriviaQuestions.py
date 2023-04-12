import discord
from discord.ext import commands
from discord import app_commands
from trivia import trivia
import asyncio


class asksTriviaQuestionCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        # TODO

    )
    async def asksTriviaQuestion(self, inter: discord.Interaction):
        trivia = await trivia.question(amount=1, category=0, quizType='multiple')
        question = trivia['question'],
        difficulty = trivia['difficulty'],
        correctAnswer = trivia['correct_answer'],
        incorrectAnswers = trivia['incorrect_answers'],
        # incorrectGuesses = [];
        id = inter.user.id

        embed = discord.Embed(
            # title=f"Trivia Question!",
            description=f"{question} \n {difficulty} \n {correctAnswer} \n {incorrectAnswers}",
            color=discord.Color.orange(),
        )

        for answers in incorrectAnswers and correctAnswer:
            view = MyView(id, answers)

        await inter.response.send_message(
            content=f"Trivia Question!", embed=embed, view=view
        )


class MyView(discord.ui.View):
    def __init__(self, creatorId, answers):
        super().__init__(timeout=None)
        self.answers = {answers}  # initialize set of answers

    @discord.ui.button(style=discord.ButtonStyle.green, label=self.answers)
    async def going(self, inter: discord.Interaction, button: discord.ui.Button):
        if self.answers == correctAnswer
            await self.updateMessageCorrect(inter)
        else:
            await self.updateMessageIncorrect(inter)

    async def updateMessageCorrect(self, inter: discord.Interaction):
        attendeesList = "\n".join(
            f"- <@{attendee}>" for attendee in self.attendees)

        embed = discord.Embed(
            title=f"Attendees ({len(self.attendees)}):",
            color=discord.Color.orange(),
            description=f"\n\n{attendeesList}",
        )
        await inter.response.edit_message(embed=embed)
    
    async def updateMessageIncorrect(self, inter: discord.Interaction):
        attendeesList = "\n".join(
            f"- <@{attendee}>" for attendee in self.attendees)

        embed = discord.Embed(
            title=f"Attendees ({len(self.attendees)}):",
            color=discord.Color.orange(),
            description=f"\n\n{attendeesList}",
        )
        await inter.response.edit_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(createStudySessionCog(bot))
