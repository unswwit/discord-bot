import discord
from discord.ext import commands
from discord import app_commands
from pyopentdb import OpenTDBClient, Category, QuestionType, Difficulty


class AskTriviaQuestionsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # Counter variable for incorrect answers
        self.incorrect_answers = 0
        self.answered_users = set()

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
    async def ask_trivia_question(
        self, inter: discord.Interaction, difficulty: app_commands.Choice[int]
    ):
        await inter.response.defer()

        # Reset the answered_users set
        self.answered_users = set()

        # Create a client to retrieve 1 "General Knowledge" question with the specified difficulty
        client = OpenTDBClient()

        if difficulty.value == 1:
            question_set = client.get_questions(
                amount=1,
                category=Category.GENERAL_KNOWLEDGE,
                difficulty=Difficulty.EASY,
            )
        elif difficulty.value == 2:
            question_set = client.get_questions(
                amount=1,
                category=Category.GENERAL_KNOWLEDGE,
                difficulty=Difficulty.MEDIUM,
            )
        elif difficulty.value == 3:
            question_set = client.get_questions(
                amount=1,
                category=Category.GENERAL_KNOWLEDGE,
                difficulty=Difficulty.HARD,
            )

        question_txt = question_set.items[0].question
        question_diff = question_set.items[0].difficulty.name.title()
        choices = question_set.items[0].choices
        answer_indx = question_set.items[0].answer_index

        embed = discord.Embed(
            title=f"Trivia Question!",
            description=f"{question_txt}",
            color=discord.Color.orange(),
        )
        embed.add_field(name="Category",
                        value=f"General Knowledge", inline=False)
        embed.add_field(name="Difficulty",
                        value=f"{question_diff}", inline=True)
        embed.add_field(
            name="Incorrect answers so far: ", value=self.incorrect_answers, inline=True
        )

        # changed from self to self.inccorect
        view = MyView(
            choices,
            answer_indx,
            question_txt,
            question_diff,
            self.incorrect_answers,
            self.answered_users,
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
        answer_indx,
        question_txt,
        question_diff,
        incorrect_answers,
        answered_users,
        disabled,
    ):
        super().__init__(timeout=None)

        self.select_menu = AnswersSelectMenu(
            choices,
            answer_indx,
            question_txt,
            question_diff,
            incorrect_answers,
            answered_users,
            disabled,
        )

        # add select menu to view
        self.add_item(self.select_menu)


class AnswersSelectMenu(discord.ui.Select):
    def __init__(
        self,
        choices,
        answer_indx,
        question_txt,
        question_diff,
        incorrect_answers,
        answered_users,
        disabled,
    ):
        self.question_txt = question_txt
        self.question_diff = question_diff
        self.choices = choices
        self.correct_choice = choices[answer_indx]
        self.answer_indx = answer_indx
        self.incorrect_answers = incorrect_answers
        self.answered_users = answered_users

        super().__init__(
            placeholder="Select a choice...",
            options=[discord.SelectOption(label=choice) for choice in choices],
            max_values=1,
            min_values=1,
        )

        self.disabled = disabled

    async def callback(self, interaction: discord.Interaction):
        user_id = interaction.user.id

        selected_choice = self.values[0]

        if user_id in self.answered_users:
            # User has already answered, send ephemeral message
            await interaction.response.send_message(
                f"You've already attempted answering this question before!",
                ephemeral=True,
            )
            return

        if selected_choice == self.correct_choice:
            # if the selected choice is correct, display a text
            await self.update_message_correct(interaction)
        else:
            self.incorrect_answers += 1
            await self.update_message_incorrect(interaction)

        # Add the user to the answered users set
        self.answered_users.add(user_id)

    async def update_message_incorrect(self, inter: discord.Interaction):
        embed = discord.Embed(
            title=f"Trivia Question!",
            description=f"{self.question_txt} \n\n Difficulty: {self.question_diff} \n\n Incorrect answers so far: {self.incorrect_answers}",
            color=discord.Color.red(),
        )
        view = MyView(
            self.choices,
            self.answer_indx,
            self.question_txt,
            self.question_diff,
            self.incorrect_answers,
            self.answered_users,
            False,
        )
        await inter.response.edit_message(embed=embed, view=view)

    async def update_message_correct(self, inter: discord.Interaction):
        embed = discord.Embed(
            title=f"Trivia Question!",
            description=f"{self.question_txt} \n\n Difficulty: {self.question_diff} \n\n <@{inter.user.id}> was the first to guess correctly! The correct answer was: {self.correct_choice} \n\n Incorrect answers so far: {self.incorrect_answers}",
            color=discord.Color.green(),
        )
        view = MyView(
            self.choices,
            self.answer_indx,
            self.question_txt,
            self.question_diff,
            self.incorrect_answers,
            self.answered_users,
            True,
        )
        await inter.response.edit_message(embed=embed, view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(AskTriviaQuestionsCog(bot))
