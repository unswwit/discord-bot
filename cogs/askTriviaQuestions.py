import discord
from discord.ext import commands
from discord import app_commands
from trivia import trivia
import asyncio


class asksTriviaQuestionCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="ask-trivia-questions",
        description="Asks trivia questions!",

    )


    async def asksTriviaQuestion(self, inter: discord.Interaction):
        trivia = await trivia.question(amount=1, category=0, quizType='multiple')
        # question = trivia['question'],
        # difficulty = trivia['difficulty'],
        # correctAnswer = trivia['correct_answer'],
        # incorrectAnswers = trivia['incorrect_answers'],
        # # incorrectGuesses = [];
        # id = inter.user.id

        # embed = discord.Embed(
        #     # title=f"Trivia Question!",
        #     description=f"{question} \n {difficulty} \n {correctAnswer} \n {incorrectAnswers}",
        #     color=discord.Color.orange(),
        # )

        # for incorrectAnswer in incorrectAnswers:
        #     view = MyView(id, incorrectAnswer, correctAnswer)

        # await inter.response.send_message(
        #     content=f"Trivia Question!", embed=embed, view=view
        # )


class MyView(discord.ui.View):
    def __init__(self, creatorId, incorrectAnswer, correctAnswer):
        super().__init__(timeout=None)
        # initialize set of answers
        self.answers = {incorrectAnswer, correctAnswer}

    @discord.ui.button(style=discord.ButtonStyle.green, label="".join(correctAnswer))
    async def correct(self, inter: discord.Interaction, button: discord.ui.Button):
        await self.updateMessageCorrect(inter)

    @discord.ui.button(style=discord.ButtonStyle.red, label="".join(incorrectAnswer))
    async def incorrect(self, inter: discord.Interaction, button: discord.ui.Button):
        await self.updateMessageIncorrect(inter)

    def __init__(self, creatorId, incorrectAnswer, correctAnswer):
        super().__init__(timeout=None)
        # initialize set of answers
        self.answers = {incorrectAnswer, correctAnswer}

    @discord.ui.button(style=discord.ButtonStyle.green, label="".join(correctAnswer))
    async def correct(self, inter: discord.Interaction, button: discord.ui.Button):
        await self.updateMessageCorrect(inter)

    @discord.ui.button(style=discord.ButtonStyle.red, label=incorrectAnswer)
    async def incorrect(self, inter: discord.Interaction, button: discord.ui.Button):
        await self.updateMessageIncorrect(inter)

    async def updateMessageCorrect(self, inter: discord.Interaction):

        embed = discord.Embed(

        )
        await inter.response.edit_message(embed=embed)

    async def updateMessageIncorrect(self, inter: discord.Interaction):

        embed = discord.Embed(

        )
        await inter.response.edit_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(asksTriviaQuestionCog(bot))

