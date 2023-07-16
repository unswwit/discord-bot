import discord
from discord.ext import commands
from discord import app_commands
from wonderwords import RandomWord

class hangmanCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="play-hangman", description="Play a game of Hangman!"
    )
    @app_commands.describe(
        category="Choose a category for the random word.",
        word_length="The length of the random word as an integer or 'Random' for any word length. (e.g. 7)"
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
        self, inter: discord.Interaction, category: app_commands.Choice[int], word_length: str
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
                await inter.followup.send("I can't generate a word unless word_length is an integer or 'Random', please try again.")
                return

        try:
            randomWord = r.word(include_parts_of_speech=selectedCategory, word_min_length=selectedLength, word_max_length=selectedLength)
        except Exception as e:
            await inter.followup.send("I can't generate a word with that word length, please try again.")
            return

        embed = discord.Embed(
            title=f"Hangman!",
            description=f"Selected category: {category.name}\nRandom word: {randomWord}",
            color=discord.Color.orange(),
        )
        view = MyView(id)
        await inter.followup.send(
            embed=embed,
            view=view,
        )

class MyView(discord.ui.View):
    def __init__(self, creatorId):
        super().__init__(timeout=None)
        self.creatorId = creatorId
        self.pages = []  # list to store button pages
        self.letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.page_size = 13  # Number of buttons per page

        self.create_buttons()
        self.split_buttons_into_pages()

        self.current_page = 0
        self.add_buttons_to_current_page()
        self.add_page_switching_buttons()

    def create_buttons(self):
        self.buttons = []
        for letter in self.letters:
            button_callback = self.create_button_callback(letter)
            button = discord.ui.Button(style=discord.ButtonStyle.green, label=letter, custom_id=letter)
            button.callback = button_callback
            self.buttons.append(button)

    def split_buttons_into_pages(self):
        self.pages = [self.buttons[i:i+self.page_size] for i in range(0, len(self.buttons), self.page_size)]

    def create_button_callback(self, button_id):
        async def button_callback(interaction):
            await self.updateMessage(interaction)
        return button_callback

    # async def updateMessage(self, interaction):

    def add_page_switching_buttons(self):
        if self.current_page > 0:
            previous_button = discord.ui.Button(style=discord.ButtonStyle.blurple, label='Previous', custom_id='previous')
            previous_button.callback = self.previous_page
            self.add_item(previous_button)

        if self.current_page < len(self.pages) - 1:
            next_button = discord.ui.Button(style=discord.ButtonStyle.blurple, label='Next', custom_id='next')
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
        await interaction.message.edit(view=self)

    def add_buttons_to_current_page(self):
        for button in self.pages[self.current_page]:
            self.add_item(button)

async def setup(bot: commands.Bot):
    await bot.add_cog(hangmanCog(bot))
