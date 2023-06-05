import discord
from discord.ext import commands
from discord import app_commands
from pyopentdb import OpenTDBClient, Category, QuestionType, Difficulty



class asksTriviaQuestionCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # Counter variable for incorrect answers
        self.incorrect_answers = 0 

    @app_commands.command(
        name="ask-trivia-questions",
        description="Asks trivia questions!"
    )
    @app_commands.describe(difficulty='choose a difficulty')
    @app_commands.choices(difficulty=[
        app_commands.Choice(name='EASY', value=1),
        app_commands.Choice(name='MEDIUM', value=2),
        app_commands.Choice(name='HARD', value=3)
    ])

    async def asksTriviaQuestion(self, inter: discord.Interaction, difficulty: app_commands.Choice[int]):
        await inter.response.defer()

        # Create a client to retrieve 1 "General Knowledge" question with the specified difficulty
        client = OpenTDBClient()

        if difficulty.value == 1:
            questionSet = client.get_questions(amount=1, category=Category.GENERAL_KNOWLEDGE, difficulty=Difficulty.EASY)
        elif difficulty.value == 2:
            questionSet = client.get_questions(amount=1, category=Category.GENERAL_KNOWLEDGE, difficulty=Difficulty.MEDIUM)
        elif difficulty.value == 3:
            questionSet = client.get_questions(amount=1, category=Category.GENERAL_KNOWLEDGE, difficulty=Difficulty.HARD)

        questionTxt = questionSet.items[0].question
        questionDiff = questionSet.items[0].difficulty.name.title()
        choices = questionSet.items[0].choices
        answerIndx = questionSet.items[0].answer_index


        embed = discord.Embed(
            # title=f"Trivia Question!",
            description=f"Question: {questionTxt} \n\n Difficulty: {questionDiff} \n\n Incorrect answers so far: {self.incorrect_answers} \n\n Choices ",
            color=discord.Color.orange(),
        )

        # print("\n\n\n\n")
        # print(questionSet)
        view = MyView(choices, answerIndx)
        await inter.response.send_message(
            content=f"Trivia Question!", 
            embed=embed,
            view=view
        )

        # Send the question as a message
        # await ctx.send(question.question)

class MyView(discord.ui.View):
    def __init__(self, choices, answerIndx, incorrect_answers):
        super().__init__(timeout=None)
        # initialize set of choices
        self.choices = choices
        self.correct_choice = choices[answerIndx]

        # create select menu with all choices
        self.select_menu = discord.ui.Select(
            placeholder='Select a choice...',
            options=[discord.SelectOption(label=choice) for choice in choices],
            max_values=1,
            min_values=1
            )

    async def callback(self, interaction: discord.Interaction):
        selected_choice = self.values[0]
        print(selected_choice)
        print(self.correct_choice)
        if selected_choice == self.correct_choice:
            # if the selected choice is correct, display a text
            await interaction.response.send_message(f"You selected the correct choice!")
        else:
            self.incorrect_answers += 1
            # if the selected choice is incorrect, do nothing
            await interaction.response.send_message(f"You selected the wrong choice!")

async def setup(bot: commands.Bot):
    await bot.add_cog(asksTriviaQuestionCog(bot))