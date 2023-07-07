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

        await inter.followup.send(
            embed=embed,
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(hangmanCog(bot))
