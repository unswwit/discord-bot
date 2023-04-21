import discord
from discord.ext import commands
from discord import app_commands
from pyopentdb import OpenTDBClient, Category, QuestionType, Difficulty



class asksTriviaQuestionCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="ask-trivia-questions",
        description="Asks trivia questions!"
    )

    async def asksTriviaQuestion(self, inter: discord.Interaction):
        # Create a client to retrieve 1 "General Knowledge" question with "medium" difficulty
        client = OpenTDBClient()
        questionSet = client.get_questions(amount=1, category=Category.GENERAL_KNOWLEDGE, difficulty=Difficulty.MEDIUM)
    
        questionTxt = questionSet.items[0].question
        questionDiff = questionSet.items[0].difficulty.name.title()
        # answerChoices = '\n'.join(questionList[0].choices)

        embed = discord.Embed(
            # title=f"Trivia Question!",
            description=f"Question: {questionTxt} \n\n\n Difficulty: {questionDiff}",
            color=discord.Color.orange(),
        )

        print(questionSet)

        # view = MyView(id)
        await inter.response.send_message(
            content=f"Trivia Question!", embed=embed
        )

        # Send the question as a message
        # await ctx.send(question.question)


        # for incorrectAnswer in incorrectAnswers:
        #     view = MyView(id, incorrectAnswer, correctAnswer)



# class MyView(discord.ui.View):
#     def __init__(self, creatorId, incorrectAnswer, correctAnswer):
#         super().__init__(timeout=None)
#         # initialize set of answers
#         self.answers = {incorrectAnswer, correctAnswer}

#     @discord.ui.button(style=discord.ButtonStyle.green, label="".join(correctAnswer))
#     async def correct(self, inter: discord.Interaction, button: discord.ui.Button):
#         await self.updateMessageCorrect(inter)

#     @discord.ui.button(style=discord.ButtonStyle.red, label="".join(incorrectAnswer))
#     async def incorrect(self, inter: discord.Interaction, button: discord.ui.Button):
#         await self.updateMessageIncorrect(inter)

#     def __init__(self, creatorId, incorrectAnswer, correctAnswer):
#         super().__init__(timeout=None)
#         # initialize set of answers
#         self.answers = {incorrectAnswer, correctAnswer}

#     @discord.ui.button(style=discord.ButtonStyle.green, label="".join(correctAnswer))
#     async def correct(self, inter: discord.Interaction, button: discord.ui.Button):
#         await self.updateMessageCorrect(inter)

#     @discord.ui.button(style=discord.ButtonStyle.red, label=incorrectAnswer)
#     async def incorrect(self, inter: discord.Interaction, button: discord.ui.Button):
#         await self.updateMessageIncorrect(inter)

#     async def updateMessageCorrect(self, inter: discord.Interaction):

#         embed = discord.Embed(

#         )
#         await inter.response.edit_message(embed=embed)

#     async def updateMessageIncorrect(self, inter: discord.Interaction):

#         embed = discord.Embed(

#         )
#         await inter.response.edit_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(asksTriviaQuestionCog(bot))

