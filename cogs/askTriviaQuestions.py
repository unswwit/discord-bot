import discord
from discord.ext import commands
from discord import app_commands
from pyopentdb import OpenTDBClient, Category, QuestionType, Difficulty


class asksTriviaQuestionCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # Counter variable for incorrect answers
        self.incorrectAnswers = 0
        self.answeredUsers = set()

    @app_commands.command(
        name="ask-trivia-questions", description="Asks trivia questions!"
    )
    @app_commands.describe(difficulty="choose a difficulty")
    @app_commands.choices(
        difficulty=[
            app_commands.Choice(name="Easy", value=1),
            app_commands.Choice(name="Medium", value=2),
            app_commands.Choice(name="Hard", value=3),
        ]
    )
    async def asksTriviaQuestion(
        self, inter: discord.Interaction, difficulty: app_commands.Choice[int]
    ):
        await inter.response.defer()

        # Reset the answered_users set
        self.answeredUsers = set()

        # Create a client to retrieve 1 "General Knowledge" question with the specified difficulty
        client = OpenTDBClient()

        if difficulty.value == 1:
            questionSet = client.get_questions(
                amount=1,
                category=Category.GENERAL_KNOWLEDGE,
                difficulty=Difficulty.EASY,
            )
        elif difficulty.value == 2:
            questionSet = client.get_questions(
                amount=1,
                category=Category.GENERAL_KNOWLEDGE,
                difficulty=Difficulty.MEDIUM,
            )
        elif difficulty.value == 3:
            questionSet = client.get_questions(
                amount=1,
                category=Category.GENERAL_KNOWLEDGE,
                difficulty=Difficulty.HARD,
            )

        questionTxt = questionSet.items[0].question
        questionDiff = questionSet.items[0].difficulty.name.title()
        choices = questionSet.items[0].choices
        answerIndx = questionSet.items[0].answer_index

        embed = discord.Embed(
            title=f"Trivia Question!",
            description=f"{questionTxt} \n\n Difficulty: {questionDiff} \n\n Incorrect answers so far: {self.incorrectAnswers}",
            color=discord.Color.orange(),
        )

        # changed from self to self.inccorect
        view = MyView(
            choices,
            answerIndx,
            questionTxt,
            questionDiff,
            self.incorrectAnswers,
            self.answeredUsers,
            False,
        )
        await inter.followup.send(
            embed=embed,
            view=view,
        )


class MyView(discord.ui.View):
    def __init__(
        self,
        choices,
        answerIndx,
        questionTxt,
        questionDiff,
        incorrectAnswers,
        answeredUsers,
        disabled,
    ):
        super().__init__(timeout=None)

        self.select_menu = AnswersSelectMenu(
            choices,
            answerIndx,
            questionTxt,
            questionDiff,
            incorrectAnswers,
            answeredUsers,
            disabled,
        )

        # add select menu to view
        self.add_item(self.select_menu)


class AnswersSelectMenu(discord.ui.Select):
    def __init__(
        self,
        choices,
        answerIndx,
        questionTxt,
        questionDiff,
        incorrectAnswers,
        answeredUsers,
        disabled,
    ):
        self.questionTxt = questionTxt
        self.questionDiff = questionDiff
        self.choices = choices
        self.correctChoice = choices[answerIndx]
        self.answerIndx = answerIndx
        self.incorrectAnswers = incorrectAnswers
        self.answeredUsers = answeredUsers

        super().__init__(
            placeholder="Select a choice...",
            options=[discord.SelectOption(label=choice) for choice in choices],
            max_values=1,
            min_values=1,
        )

        self.disabled = disabled

    async def callback(self, interaction: discord.Interaction):
        userId = interaction.user.id

        selectedChoice = self.values[0]

        if userId in self.answeredUsers:
            # User has already answered, send ephemeral message
            await interaction.response.send_message(
                f"You've already attempted answering this question before!",
                ephemeral=True,
            )
            return

        if selectedChoice == self.correctChoice:
            # if the selected choice is correct, display a text
            await self.updateMessageCorrect(interaction)
        else:
            self.incorrectAnswers += 1
            await self.updateMessageIncorrect(interaction)

        self.answeredUsers.add(userId)  # Add the user to the answered users set

    async def updateMessageIncorrect(self, inter: discord.Interaction):
        embed = discord.Embed(
            title=f"Trivia Question!",
            description=f"{self.questionTxt} \n\n Difficulty: {self.questionDiff} \n\n Incorrect answers so far: {self.incorrectAnswers}",
            color=discord.Color.red(),
        )
        view = MyView(
            self.choices,
            self.answerIndx,
            self.questionTxt,
            self.questionDiff,
            self.incorrectAnswers,
            self.answeredUsers,
            False,
        )
        await inter.response.edit_message(embed=embed, view=view)

    async def updateMessageCorrect(self, inter: discord.Interaction):
        embed = discord.Embed(
            title=f"Trivia Question!",
            description=f"{self.questionTxt} \n\n Difficulty: {self.questionDiff} \n\n <@{inter.user.id}> was the first to guess correctly! The correct answer was: {self.correctChoice} \n\n Incorrect answers so far: {self.incorrectAnswers}",
            color=discord.Color.green(),
        )
        view = MyView(
            self.choices,
            self.answerIndx,
            self.questionTxt,
            self.questionDiff,
            self.incorrectAnswers,
            self.answeredUsers,
            True,
        )
        await inter.response.edit_message(embed=embed, view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(asksTriviaQuestionCog(bot))
