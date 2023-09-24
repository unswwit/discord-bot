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
    9: Category.ENTERTAINMENT_COMICS,
    10: Category.ENTERTAINMENT_JAPANESE_ANIME_MANGA,
    11: Category.ENTERTAINMENT_CARTOON_ANIMATIONS,
    12: Category.SCIENCE_COMPUTERS,
    13: Category.SCIENCE_GADGETS,
    14: Category.SCIENCE_NATURE,
    15: Category.MYTHOLOGY,
    16: Category.SPORTS,
    17: Category.GEOGRAPHY,
    18: Category.HISTORY,
    19: Category.POLITICS,
    20: Category.ART,
    21: Category.CELEBRITIES,
    22: Category.ANIMALS,
    23: Category.VEHICLES,
}

category_names = {
    Category.GENERAL_KNOWLEDGE: "General Knowledge",
    Category.ENTERTAINMENT_BOOKS: "Entertainment: Books",
    Category.ENTERTAINMENT_FILM: "Entertainment: Film",
    Category.ENTERTAINMENT_MUSIC: "Entertainment: Music",
    Category.ENTERTAINMENT_MUSICALS_THEATRES: "Entertainment: Musical Theatres",
    Category.ENTERTAINMENT_TELEVISION: "Entertainment: Television",
    Category.ENTERTAINMENT_VIDEO_GAMES: "Entertainment: Video Games",
    Category.ENTERTAINMENT_BOARD_GAMES: "Entertainment: Board Games",
    Category.ENTERTAINMENT_COMICS: "Entertainment: Comics",
    Category.ENTERTAINMENT_JAPANESE_ANIME_MANGA: "Entertainment: Japanese Anime Manga",
    Category.ENTERTAINMENT_CARTOON_ANIMATIONS: "Entertainment: Cartoon Animations",
    Category.SCIENCE_COMPUTERS: "Science: Computers",
    Category.SCIENCE_GADGETS: "Science: Gadgets",
    Category.SCIENCE_NATURE: "Science: Nature",
    Category.MYTHOLOGY: "Mythology",
    Category.SPORTS: "Sports",
    Category.GEOGRAPHY: "Geography",
    Category.HISTORY: "History",
    Category.POLITICS: "Politics",
    Category.ART: "Art",
    Category.CELEBRITIES: "Celebrities",
    Category.ANIMALS: "Animals",
    Category.VEHICLES: "Vehicles",
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
            app_commands.Choice(name="Entertainment: Comics", value=9),
            app_commands.Choice(
                name="Entertainment: Japanese Anime & Manga", value=10),
            app_commands.Choice(
                name="Entertainment: Cartoon & Animations", value=11),
            app_commands.Choice(name="Science: Computers", value=12),
            app_commands.Choice(name="Science: Gadgets", value=13),
            app_commands.Choice(name="Science: Nature", value=14),
            app_commands.Choice(name="Mythology", value=15),
            app_commands.Choice(name="Sports", value=16),
            app_commands.Choice(name="Geography", value=17),
            app_commands.Choice(name="History", value=18),
            app_commands.Choice(name="Politics", value=19),
            app_commands.Choice(name="Art", value=20),
            app_commands.Choice(name="Celebrities", value=21),
            app_commands.Choice(name="Animals", value=22),
            app_commands.Choice(name="Vehicles", value=23),
        ],
    )
    async def ask_trivia_question(
        self,
        interaction: discord.Interaction,
        difficulty: app_commands.Choice[int],
        category: app_commands.Choice[int],
    ):
        await interaction.response.defer()

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
            title="Trivia Question!",
            description=question_txt,
            color=discord.Color.orange(),
        )
        embed.add_field(
            name="Category", value=category_names.get(selected_category), inline=True
        )
        embed.add_field(name="Difficulty", value=question_diff, inline=True)
        embed.add_field(
            name="Incorrect answers so far: ",
            value=self.incorrect_answers,
            inline=False,
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
        await interaction.followup.send(
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

    async def update_message_incorrect(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=f"Trivia Question!",
            description=f"{self.question_txt}",
            color=discord.Color.red(),
        )
        embed.add_field(
            name="Category",
            value=f"{category_names.get(self.selected_category)}",
            inline=True,
        )
        embed.add_field(name="Difficulty",
                        value=f"{self.question_diff}", inline=True)
        embed.add_field(
            name="Incorrect answers so far: ",
            value=f"{self.incorrect_answers}",
            inline=False,
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
        await interaction.response.edit_message(embed=embed, view=view)

    async def update_message_correct(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=f"Trivia Question!",
            description=f"{self.question_txt}",
            color=discord.Color.green(),
        )
        embed.add_field(
            name="Category",
            value=f"{category_names.get(self.selected_category)}",
            inline=True,
        )
        embed.add_field(name="Difficulty",
                        value=f"{self.question_diff}", inline=True)
        embed.add_field(
            name="",
            value=f"<@{interaction.user.id}> was the first to guess correctly! The correct answer was: {self.correct_choice}",
            inline=False,
        )
        embed.add_field(
            name="Incorrect answers so far: ",
            value=f"{self.incorrect_answers}",
            inline=False,
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
        await interaction.response.edit_message(embed=embed, view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(AskTriviaQuestionsCog(bot))
