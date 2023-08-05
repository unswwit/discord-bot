import discord
import string
from discord.ext import commands
from discord import app_commands
from wonderwords import RandomWord


class hangmanCog(commands.Cog):
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
    async def playHangman(
        self,
        inter: discord.Interaction,
        category: app_commands.Choice[int],
        word_length: str,
    ):
        await inter.response.defer()
        r = RandomWord()

        if category.value == 1:
            selectedCategory = ["nouns"]
        elif category.value == 2:
            selectedCategory = ["adjectives"]
        elif category.value == 3:
            selectedCategory = ["verbs"]
        else:
            selectedCategory = None

        if word_length.lower() == "random":
            selectedLength = None
        else:
            try:
                selectedLength = int(word_length)
            except ValueError:
                await inter.followup.send(
                    "I can't generate a word unless word_length is an integer or 'Random', please try again."
                )
                return

        try:
            randomWord = r.word(
                include_parts_of_speech=selectedCategory,
                word_min_length=selectedLength,
                word_max_length=selectedLength,
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
            value=f"```{' '.join('_' for c in randomWord)}```",
            inline=False,
        )

        view = MyView(id, randomWord, category.name)
        await inter.followup.send(
            embed=embed,
            view=view,
        )


class MyView(discord.ui.View):
    def __init__(self, creatorId, randomWord, category):
        super().__init__(timeout=None)
        self.creatorId = creatorId
        self.randomWord = randomWord.upper()
        self.revealedWord = "".join("_" for c in self.randomWord)
        self.incorrectLetters = []
        self.pages = []  # list to store button pages
        self.pageSize = 13  # Number of buttons per page
        self.category = category
        self.createButtons()
        self.splitButtonsIntoPages()
        self.currentPage = 0
        self.addButtonsToCurrentPage()
        self.addPageSwitchingButtons()
        self.hangmanStages = [
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

    def createButtons(self):
        self.buttons = []
        for letter in list(string.ascii_uppercase):
            buttonCallback = self.createButtonCallback(letter)
            button = discord.ui.Button(
                style=discord.ButtonStyle.green, label=letter, custom_id=letter
            )
            button.callback = buttonCallback
            self.buttons.append(button)

    def splitButtonsIntoPages(self):
        self.pages = [
            self.buttons[i : i + self.pageSize]
            for i in range(0, len(self.buttons), self.pageSize)
        ]

    def createButtonCallback(self, button_id):
        # Runs when a letter is pressed to update hangman state
        async def buttonCallback(interaction):
            for item in self.children:
                if item.custom_id == button_id:
                    item.disabled = True
                    if not self.guessIsCorrect(button_id):
                        self.incorrectLetters.append(button_id)
            if len(self.incorrectLetters) == 6 or self.randomWord == self.revealedWord:
                for item in self.children:
                    # Game has ended, disable all buttons
                    item.disabled = True

            await self.updateMessage(interaction, button_id)

        return buttonCallback

    def guessIsCorrect(self, guess):
        correct = guess in self.randomWord
        if correct:
            self.revealedWord = "".join(
                c if c == guess else r
                for c, r in zip(self.randomWord, self.revealedWord)
            )
        return correct

    async def updateMessage(self, interaction, button_id):
        # Create a new embed with the updated information
        incorrectLettersString = (
            "None"
            if len(self.incorrectLetters) == 0
            else f"{(', '.join(c for c in self.incorrectLetters))}"
        )

        embed = discord.Embed(
            title="Hangman!",
            description=f"{self.hangmanStages[min(len(self.incorrectLetters), len(self.hangmanStages)-1)]}",
            color=discord.Color.orange(),
        )
        embed.add_field(name="Category", value=f"{self.category}", inline=False)
        embed.add_field(
            name="Incorrect Guesses",
            value=f"{len(self.incorrectLetters)}/6",
            inline=True,
        )
        embed.add_field(
            name="Incorrect Letters", value=incorrectLettersString, inline=True
        )
        embed.add_field(
            name="Word", value=f"```{' '.join(self.revealedWord)}```", inline=False
        )

        if len(self.incorrectLetters) == 6:
            # Game is lost
            embed.add_field(
                name="Game Lost!",
                value=f"The word was: {self.randomWord}",
                inline=False,
            )
        elif self.randomWord == self.revealedWord:
            # Game is won
            embed.add_field(
                name="Game Won!",
                value=f"The final guesser was: <@{interaction.user.id}>",
                inline=False,
            )

        # Update the message with the new embed
        await interaction.response.edit_message(embed=embed, view=self)

    def addPageSwitchingButtons(self):
        if self.currentPage > 0:
            previousButton = discord.ui.Button(
                style=discord.ButtonStyle.blurple,
                label="Previous",
                custom_id="previous",
            )
            previousButton.callback = self.previous_page
            self.add_item(previousButton)

        if self.currentPage < len(self.pages) - 1:
            nextButton = discord.ui.Button(
                style=discord.ButtonStyle.blurple, label="Next", custom_id="next"
            )
            nextButton.callback = self.next_page
            self.add_item(nextButton)

    async def previous_page(self, interaction):
        if self.currentPage > 0:
            self.currentPage -= 1
            await self.updateView(interaction)

    async def next_page(self, interaction):
        if self.currentPage < len(self.pages) - 1:
            self.currentPage += 1
            await self.updateView(interaction)

    async def updateView(self, interaction):
        self.clear_items()
        self.addButtonsToCurrentPage()
        self.addPageSwitchingButtons()
        await interaction.response.edit_message(view=self)

    def addButtonsToCurrentPage(self):
        for button in self.pages[self.currentPage]:
            self.add_item(button)


async def setup(bot: commands.Bot):
    await bot.add_cog(hangmanCog(bot))