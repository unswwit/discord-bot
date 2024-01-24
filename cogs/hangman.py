import discord
import string
from discord.ext import commands
from discord import app_commands
from wonderwords import RandomWord

from oweek_ctf import run_ctf

class HangmanCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="play-hangman", description="Play a game of Hangman!")
    @app_commands.describe(
        category="Choose a category for the random word.",
        word_length="The length of the random word as an integer or 'Random' for any word length. (e.g. 7)",
    )
    @app_commands.choices(
        category=[
            app_commands.Choice(name="Noun", value=1),
            app_commands.Choice(name="Adjective", value=2),
            app_commands.Choice(name="Verb", value=3),
            app_commands.Choice(name="Random", value=4),
        ],
    )
    async def play_hangman(
        self,
        inter: discord.Interaction,
        category: app_commands.Choice[int],
        word_length: str,
    ):
        await inter.response.defer()

        if category.value == 1:
            selected_category = ["nouns"]
        elif category.value == 2:
            selected_category = ["adjectives"]
        elif category.value == 3:
            selected_category = ["verbs"]
        else:
            selected_category = None

        if word_length.lower() == "random":
            selected_length = None
        else:
            try:
                selected_length = int(word_length)
            except ValueError:
                await inter.followup.send(
                    "I can't generate a word unless word_length is an integer or 'Random', please try again."
                )
                return

        r = RandomWord()
        try:
            random_word = r.word(
                include_parts_of_speech=selected_category,
                word_min_length=selected_length,
                word_max_length=selected_length,
            )
        except Exception as e:
            await inter.followup.send(
                "I can't generate a word with that word length, please try again."
            )
            return

        embed = discord.Embed(
            title=f"Hangman!",
            description=f""
            "```\n"
            "   +----+\n"
            "   |    |\n"
            "   |   \n"
            "   |   \n"
            "   |   \n"
            "   ===\n"
            "```",
            color=discord.Color.orange(),
        )
        embed.add_field(name="Category", value=f"{category.name}", inline=False)
        embed.add_field(name="Incorrect Guesses", value="0/6", inline=True)
        embed.add_field(name="Incorrect Letters", value=f"None", inline=True)
        embed.add_field(
            name="Word",
            value=f"```{' '.join('_' for c in random_word)}```",
            inline=False,
        )

        view = MyView(id, random_word, category.name)
        await inter.followup.send(
            embed=embed,
            view=view,
        )

        # Run O-Week CTF
        await run_ctf(inter.user)


class MyView(discord.ui.View):
    def __init__(self, creator_id, random_word, category):
        super().__init__(timeout=None)
        self.creator_id = creator_id
        self.random_word = random_word.upper()
        self.revealed_word = "".join("_" for c in self.random_word)
        self.incorrect_letters = []
        self.pages = []  # list to store button pages
        self.page_size = 13  # Number of buttons per page
        self.category = category
        self.create_buttons()
        self.split_buttons_into_pages()
        self.current_page = 0
        self.add_buttons_to_current_page()
        self.add_page_switching_buttons()
        self.hangman_stages = [
            "```\n"
            "   +----+\n"
            "   |    |\n"
            "   |   \n"
            "   |   \n"
            "   |   \n"
            "   ===\n"
            "```",  # 0 wrong
            "```\n"
            "   +----+\n"
            "   |    |\n"
            "   |    O\n"
            "   |   \n"
            "   |   \n"
            "   ===\n"
            "```",  # 1 wrong
            "```\n"
            "   +----+\n"
            "   |    |\n"
            "   |    O\n"
            "   |    |\n"
            "   |   \n"
            "   ===\n"
            "```",  # 2 wrong
            "```\n"
            "   +----+\n"
            "   |    |\n"
            "   |    O\n"
            "   |    |\\\n"
            "   |   \n"
            "   ===\n"
            "```",  # 3 wrong
            "```\n"
            "   +----+\n"
            "   |    |\n"
            "   |    O\n"
            "   |   /|\\\n"
            "   |   \n"
            "   ===\n"
            "```",  # 4 wrong
            "```\n"
            "   +----+\n"
            "   |    |\n"
            "   |    O\n"
            "   |   /|\\\n"
            "   |     \\\n"
            "   === \n"
            "```",  # 5 wrong
            "```\n"
            "   +----+\n"
            "   |    |\n"
            "   |    O\n"
            "   |   /|\\\n"
            "   |   / \\\n"
            "   === \n"
            "```",  # 6 wrong
        ]

    def create_buttons(self):
        self.buttons = []
        for letter in list(string.ascii_uppercase):
            button_callback = self.create_button_callback(letter)
            button = discord.ui.Button(
                style=discord.ButtonStyle.green, label=letter, custom_id=letter
            )
            button.callback = button_callback
            self.buttons.append(button)

    def split_buttons_into_pages(self):
        self.pages = [
            self.buttons[i : i + self.page_size]
            for i in range(0, len(self.buttons), self.page_size)
        ]

    def create_button_callback(self, button_id):
        # Runs when a letter is pressed to update hangman state
        async def button_callback(interaction):
            for item in self.children:
                if item.custom_id == button_id:
                    item.disabled = True
                    if not self.guess_is_correct(button_id):
                        self.incorrect_letters.append(button_id)
            if (
                len(self.incorrect_letters) == 6
                or self.random_word == self.revealed_word
            ):
                for item in self.children:
                    # Game has ended, disable all buttons
                    item.disabled = True

            await self.update_message(interaction, button_id)

        return button_callback

    def guess_is_correct(self, guess):
        correct = guess in self.random_word
        if correct:
            self.revealed_word = "".join(
                c if c == guess else r
                for c, r in zip(self.random_word, self.revealed_word)
            )
        return correct

    async def update_message(self, interaction, button_id):
        # Create a new embed with the updated information
        incorrect_letters_string = (
            "None"
            if len(self.incorrect_letters) == 0
            else f"{(', '.join(c for c in self.incorrect_letters))}"
        )

        embed = discord.Embed(
            title="Hangman!",
            description=f"{self.hangman_stages[min(len(self.incorrect_letters), len(self.hangman_stages)-1)]}",
            color=discord.Color.orange(),
        )
        embed.add_field(name="Category", value=f"{self.category}", inline=False)
        embed.add_field(
            name="Incorrect Guesses",
            value=f"{len(self.incorrect_letters)}/6",
            inline=True,
        )
        embed.add_field(
            name="Incorrect Letters", value=incorrect_letters_string, inline=True
        )
        embed.add_field(
            name="Word", value=f"```{' '.join(self.revealed_word)}```", inline=False
        )

        if len(self.incorrect_letters) == 6:
            # Game is lost
            embed.add_field(
                name="Game Lost!",
                value=f"The word was: {self.random_word}",
                inline=False,
            )
        elif self.random_word == self.revealed_word:
            # Game is won
            embed.add_field(
                name="Game Won!",
                value=f"The final guesser was: <@{interaction.user.id}>",
                inline=False,
            )

        # Update the message with the new embed
        await interaction.response.edit_message(embed=embed, view=self)

    def add_page_switching_buttons(self):
        if self.current_page > 0:
            previous_button = discord.ui.Button(
                style=discord.ButtonStyle.blurple,
                label="Previous",
                custom_id="previous",
            )
            previous_button.callback = self.previous_page
            self.add_item(previous_button)

        if self.current_page < len(self.pages) - 1:
            next_button = discord.ui.Button(
                style=discord.ButtonStyle.blurple, label="Next", custom_id="next"
            )
            next_button.callback = self.next_page
            self.add_item(next_button)

    async def previous_page(self, interaction):
        if self.current_page > 0:
            self.current_page -= 1
            await self.update_view(interaction)

    async def next_page(self, interaction):
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            await self.update_view(interaction)

    async def update_view(self, interaction):
        self.clear_items()
        self.add_buttons_to_current_page()
        self.add_page_switching_buttons()
        await interaction.response.edit_message(view=self)

    def add_buttons_to_current_page(self):
        for button in self.pages[self.current_page]:
            self.add_item(button)


async def setup(bot: commands.Bot):
    await bot.add_cog(HangmanCog(bot))
