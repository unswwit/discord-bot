import discord
from discord.ext import commands
from discord import app_commands
from pyopentdb import OpenTDBClient, Category, QuestionType, Difficulty

# Define category values
category_mapping = {
    1: Category.GENERAL_KNOWLEDGE,
    2: Category.ENTERTAINMENT_BOOKS,
    3: Category.ENTERTAINMENT_FILM,
    4: Category.ENTERTAINMENT_MUSIC,
    5: Category.ENTERTAINMENT_MUSICALS_THEATRES,
    6: Category.ENTERTAINMENT_TELEVISION,
    7: Category.ENTERTAINMENT_VIDEO_GAMES,
    8: Category.ENTERTAINMENT_BOARD_GAMES,
    9: Category.SCIENCE_NATURE,
    10: Category.SCIENCE_COMPUTERS,
    11: Category.MYTHOLOGY,
    12: Category.SPORTS,
    13: Category.GEOGRAPHY,
    14: Category.HISTORY,
    15: Category.POLITICS,
    16: Category.ART,
    17: Category.CELEBRITIES,
    18: Category.ANIMALS,
    19: Category.VEHICLES,
    20: Category.ENTERTAINMENT_COMICS,
    21: Category.SCIENCE_GADGETS,
    22: Category.ENTERTAINMENT_JAPANESE_ANIME_MANGA,
    23: Category.ENTERTAINMENT_CARTOON_ANIMATIONS,
}


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
    @app_commands.describe(category="choose a category")
    @app_commands.choices(
        difficulty=[
            app_commands.Choice(name="Easy", value=1),
            app_commands.Choice(name="Medium", value=2),
            app_commands.Choice(name="Hard", value=3),
        ],
        category=[
            app_commands.Choice(name="General Knowledge", value=1),
            app_commands.Choice(name="Entertainment: Books", value=2),
            app_commands.Choice(name="Entertainment: Film", value=3),
            app_commands.Choice(name="Entertainment: Music", value=4),
            app_commands.Choice(
                name="Entertainment: Musicals & Theatres", value=5),
            app_commands.Choice(name="Entertainment: Television", value=6),
            app_commands.Choice(name="Entertainment: Video Games", value=7),
            app_commands.Choice(name="Entertainment: Board Games", value=8),
            app_commands.Choice(name="Science & Nature", value=9),
            app_commands.Choice(name="Science: Computers", value=10),
            app_commands.Choice(name="Mythology", value=11),
            app_commands.Choice(name="Sports", value=12),
            app_commands.Choice(name="Geography", value=13),
            app_commands.Choice(name="History", value=14),
            app_commands.Choice(name="Politics", value=15),
            app_commands.Choice(name="Art", value=16),
            app_commands.Choice(name="Celebrities", value=17),
            app_commands.Choice(name="Animals", value=18),
            app_commands.Choice(name="Vehicles", value=19),
            app_commands.Choice(name="Entertainment: Comics", value=20),
            app_commands.Choice(name="Science: Gadgets", value=21),
            app_commands.Choice(
                name="Entertainment: Japanese Anime & Manga", value=22),
            app_commands.Choice(
                name="Entertainment: Cartoon & Animations", value=23),
        ],
    )
    async def ask_trivia_question(
        self,
        inter: discord.Interaction,
        difficulty: app_commands.Choice[int],
        category: app_commands.Choice[int],
    ):
        await inter.response.defer()

        # Reset the answered_users set
        self.answered_users = set()

        # Convert the selected category value to value
        selected_category = category_mapping.get(category.value, None)

        # Create a client to retrieve 1 question with the specified difficulty and category
        client = OpenTDBClient()

        if difficulty.value == 1:
            question_set = client.get_questions(
                amount=1,
                category=selected_category,
                difficulty=Difficulty.EASY,
            )
        elif difficulty.value == 2:
            question_set = client.get_questions(
                amount=1,
                category=selected_category,
                difficulty=Difficulty.MEDIUM,
            )
        elif difficulty.value == 3:
            question_set = client.get_questions(
                amount=1,
                category=selected_category,
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
                        value=f"{selected_category}", inline=True)
        embed.add_field(name="Difficulty",
                        value=f"{question_diff}", inline=True)
        embed.add_field(
            name="Incorrect answers so far: ", value=self.incorrect_answers, inline=True
        )

        # changed from self to self.incorrect
        view = MyView(
            choices,
            answer_indx,
            question_txt,
            question_diff,
            self.incorrect_answers,
            self.answered_users,
            False,
            selected_category,
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
        selected_category,
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
            selected_category,
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
        selected_category,
    ):
        self.question_txt = question_txt
        self.question_diff = question_diff
        self.choices = choices
        self.correct_choice = choices[answer_indx]
        self.answer_indx = answer_indx
        self.incorrect_answers = incorrect_answers
        self.answered_users = answered_users
        self.selected_category = selected_category

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
            description=f"{self.question_txt} \n\n Difficulty: {self.question_diff} \n\n Category: {self.selected_category.name.title().replace('_', ' ')} \n\n Incorrect answers so far: {self.incorrect_answers}",
            color=discord.Color.red(),
        )
        view = MyView(
            self.choices,
            self.answer_indx,
            self.question_txt,
            self.question_diff,
            self.incorrect_answers,
            self.answered_users,
            self.selected_category,
            False,
        )
        await inter.response.edit_message(embed=embed, view=view)

    async def update_message_correct(self, inter: discord.Interaction):
        embed = discord.Embed(
            title=f"Trivia Question!",
            description=f"{self.question_txt} \n\n Difficulty: {self.question_diff} \n\n Category: {self.selected_category.name.title().replace('_', ' ')} \n\n <@{inter.user.id}> was the first to guess correctly! The correct answer was: {self.correct_choice} \n\n Incorrect answers so far: {self.incorrect_answers}",
            color=discord.Color.green(),
        )
        view = MyView(
            self.choices,
            self.answer_indx,
            self.question_txt,
            self.question_diff,
            self.incorrect_answers,
            self.answered_users,
            self.selected_category,
            True,
        )
        await inter.response.edit_message(embed=embed, view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(AskTriviaQuestionsCog(bot))
