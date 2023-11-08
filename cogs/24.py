import discord
import math
import random
from discord.ext import commands
from discord import app_commands

# 24 game
# /24 to play game
# Give us 4 random numbers that can make 24
# Numpad (4x3) of only those 4 numbers, + arithmetic, brackets, equals
# Clicking equals runs solver command to see if statement makes 24
# Correct window
# Incorrect windowx

# Print random numbers that can be used to create 24
arrays_24 = [
    [1, 2, 3, 4],
    [1, 2, 3, 5],
    [1, 2, 3, 6],
    [1, 2, 3, 7],
    [1, 2, 3, 8],
    [1, 2, 3, 9],
    [1, 2, 4, 5],
    [1, 2, 4, 6],
    [1, 2, 4, 7],
    [1, 2, 4, 8],
    [1, 2, 4, 9],
    [1, 2, 5, 6],
    [1, 2, 5, 7],
    [1, 2, 5, 8],
    [1, 2, 5, 9],
    [1, 2, 6, 7],
    [1, 2, 6, 8],
    [1, 2, 6, 9],
    [1, 2, 7, 9],
    [1, 2, 8, 9],
    [1, 3, 4, 5],
    [1, 3, 4, 6],
    [1, 3, 4, 7],
    [1, 3, 4, 8],
    [1, 3, 4, 9],
    [1, 3, 5, 6],
    [1, 3, 5, 7],
    [1, 3, 5, 8],
    [1, 3, 5, 9],
    [1, 3, 6, 9],
    [1, 3, 7, 8],
    [1, 3, 7, 9],
    [1, 3, 8, 9],
    [1, 4, 5, 6],
    [1, 4, 5, 7],
    [1, 4, 5, 8],
    [1, 4, 5, 9],
    [1, 4, 6, 7],
    [1, 4, 6, 8],
    [1, 4, 6, 9],
    [1, 4, 7, 8],
    [1, 4, 7, 9],
    [1, 4, 8, 9],
    [1, 5, 6, 7],
    [1, 5, 6, 8],
    [1, 5, 6, 9],
    [1, 5, 7, 8],
    [1, 5, 7, 9],
    [1, 5, 8, 9],
    [1, 6, 7, 9],
    [1, 6, 8, 9],
    [1, 7, 8, 9],
    [2, 3, 4, 5],
    [2, 3, 4, 6],
    [2, 3, 4, 7],
    [2, 3, 4, 8],
    [2, 3, 4, 9],
    [2, 3, 5, 6],
    [2, 3, 5, 7],
    [2, 3, 5, 8],
    [2, 3, 5, 9],
    [2, 3, 6, 7],
    [2, 3, 6, 8],
    [2, 3, 6, 9],
    [2, 3, 7, 8],
    [2, 3, 7, 9],
    [2, 4, 5, 6],
    [2, 4, 5, 7],
    [2, 4, 5, 8],
    [2, 4, 5, 9],
    [2, 4, 6, 7],
    [2, 4, 6, 8],
    [2, 4, 6, 9],
    [2, 4, 7, 8],
    [2, 4, 7, 9],
    [2, 4, 8, 9],
    [2, 5, 6, 7],
    [2, 5, 6, 8],
    [2, 5, 6, 9],
    [2, 5, 7, 8],
    [2, 5, 7, 9],
    [2, 5, 8, 9],
    [2, 6, 7, 8],
    [2, 6, 7, 9],
    [2, 6, 8, 9],
    [2, 7, 8, 9],
    [3, 4, 5, 6],
    [3, 4, 5, 7],
    [3, 4, 5, 8],
    [3, 4, 5, 9],
    [3, 4, 6, 8],
    [3, 4, 6, 9],
    [3, 4, 7, 8],
    [3, 4, 7, 9],
    [3, 4, 8, 9],
    [3, 5, 6, 7],
    [3, 5, 6, 8],
    [3, 5, 6, 9],
    [3, 5, 7, 8],
    [3, 5, 7, 9],
    [3, 5, 8, 9],
    [3, 6, 7, 8],
    [3, 6, 7, 9],
    [3, 6, 8, 9],
    [3, 7, 8, 9],
    [4, 5, 6, 7],
    [4, 5, 6, 8],
    [4, 5, 6, 9],
    [4, 5, 7, 8],
    [4, 5, 7, 9],
    [4, 6, 7, 8],
    [4, 6, 7, 9],
    [4, 6, 8, 9],
    [4, 7, 8, 9],
    [5, 6, 7, 8],
    [5, 6, 7, 9],
    [5, 6, 8, 9],
    [6, 7, 8, 9],
]

class TwentyFourCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="24", description="Play a game of 24")
    async def play_24(
        self,
        interaction: discord.Interaction,
    ):
        await interaction.response.defer()

        try:
            random_combination = random.choice(arrays_24)
        except Exception as e:
            await interaction.followup.send(
                "I can't generate 4 numbers that can make 24, please try again."
            )
            return

        embed = discord.Embed(
            title="24",
            color=discord.Color.orange()
        )

        embed.add_field(
            name="Your numbers are:",
            value=f"` {random_combination[0]}   {random_combination[1]}   {random_combination[2]}   {random_combination[3]} `",
            inline=False,
        )

        view = MyView(id, random_combination)
        await interaction.followup.send(
            embed=embed,
            view=view,
            ephemeral=True
        )

class MyView(discord.ui.View):
    def __init__(self, creator_id, numbers):
        super().__init__(timeout=None)
        self.creator_id = creator_id
        self.numbers = [str(number) for number in numbers]
        self.buttons = []
        self.create_buttons()
        self.current_input = " "

    def create_buttons(self):
        # number buttons
        for number in self.numbers:
            button_callback = self.create_button_callback(number)
            button = discord.ui.Button(
                style=discord.ButtonStyle.green,
                label=number,
                custom_id=number,
                row=0,
            )
            button.callback = button_callback
            self.buttons.append(button)

        # calculator buttons
        calculator_operations = ["+", "-", "×", "÷", "(", ")", "=", "⌫"]
        cur_row = 1
        colour = discord.ButtonStyle.grey
        for operation in calculator_operations:
            # parentheses and equals on a new row
            if operation == "(":
                cur_row += 1
            elif operation == "=":
                colour = discord.ButtonStyle.blurple
            elif operation == "⌫":
                colour = discord.ButtonStyle.red

            button_callback = self.create_button_callback(operation)
            button = discord.ui.Button(
                style=colour,
                label=operation, custom_id=operation,
                row=cur_row,
            )
            button.callback = button_callback
            self.buttons.append(button)

        for button in self.buttons:
            self.add_item(button)

    def create_button_callback(self, button_id):
        # Runs when a button is pressed
        async def button_callback(interaction):
            if button_id == "⌫" and len(self.current_input) > 1:
                self.current_input = self.current_input[:-2]
            if button_id == "=":
                current_input_math = self.current_input.replace("×", "*").replace("÷", "/").replace(" ", "")
                print(eval(current_input_math))
                current_input_numbers = ''.join(filter(str.isdigit, current_input_math))
                if len(current_input_numbers) < 4:
                    await self.update_message_incorrect(interaction, "You didn't use all the numbers!")
                if len(current_input_numbers) > 4:
                    await self.update_message_incorrect(interaction, "You used too many numbers! Be sure to use 1 of each!")
                elif eval(current_input_math) == 24:
                    await self.update_message_correct(interaction)
                elif eval(current_input_math) != 24:
                    await self.update_message_incorrect(interaction, "Sorry, that's not 24!")
            elif button_id != "⌫" and button_id != "=":
                # Append the button_id to the current_input
                self.current_input += button_id + " "

            # Removing to implement delete button functionality
            # for item in self.children:
            #     if item.custom_id == button_id:
            #         # disable button if a number
            #         if button_id in self.numbers:
            #             item.disabled = True

            await self.update_message(interaction)

        return button_callback

    async def update_message(self, interaction):
        embed = discord.Embed(
            title="24",
            color=discord.Color.orange()
        )

        embed.add_field(
            name="Your numbers are:",
            value=f"` {self.numbers[0]}   {self.numbers[1]}   {self.numbers[2]}   {self.numbers[3]} `",
            inline=False,
        )

        embed.add_field(
            name="Input:", value="`" + self.current_input + "`", inline=False
        )
        await interaction.response.edit_message(embed=embed, view=self)

    async def update_message_correct(self, interaction):
        self.clear_items()
        embed = discord.Embed(
            title="24",
            color=discord.Color.green()
        )

        embed.add_field(
            name="Your numbers are:",
            value=f"` {self.numbers[0]}   {self.numbers[1]}   {self.numbers[2]}   {self.numbers[3]} `",
            inline=False,
        )

        embed.add_field(
            name="Input:", value="`" + self.current_input + "`", inline=False
        )

        embed.add_field(
            name="", value="Congrats! You made 24!", inline=False
        )

        await interaction.response.edit_message(embed=embed, view=self)

    async def update_message_incorrect(self, interaction, message):
        embed = discord.Embed(
            title="24",
            color=discord.Color.red()
        )

        embed.add_field(
            name="Your numbers are:",
            value=f"` {self.numbers[0]}   {self.numbers[1]}   {self.numbers[2]}   {self.numbers[3]} `",
            inline=False,
        )

        embed.add_field(
            name="Input:", value="`" + self.current_input + "`", inline=False
        )

        embed.add_field(
            name="", value=message, inline=False
        )
        await interaction.response.edit_message(embed=embed, view=self)

async def setup(bot: commands.Bot):
    await bot.add_cog(TwentyFourCog(bot))