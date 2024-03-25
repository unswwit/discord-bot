

import re
import discord
import math
import random
from discord.ext import commands
from discord import app_commands

# TODO: Move arrays_24 to a different file and import it here
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

        embed = discord.Embed(title="Make 24!", color=discord.Color.orange())

        embed.add_field(
            name="Your numbers are:",
            value=f"` {random_combination[0]}   {random_combination[1]}   {random_combination[2]}   {random_combination[3]} `",
            inline=False,
        )

        view = MyView(id, random_combination)
        await interaction.followup.send(embed=embed, view=view, ephemeral=True)


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
                label=operation,
                custom_id=operation,
                row=cur_row,
            )
            button.callback = button_callback
            self.buttons.append(button)

        for button in self.buttons:
            self.add_item(button)

    def create_button_callback(self, button_id):
        def isBalanced(myStr):
            open_list = ["("]
            close_list = [")"]
            stack = []
            for i in myStr:
                if i in open_list:
                    stack.append(i)
                elif i in close_list:
                    pos = close_list.index(i)
                    if ((len(stack) > 0) and
                        (open_list[pos] == stack[len(stack)-1])):
                        stack.pop()
                    else:
                        return False
            if len(stack) == 0:
                return True
            else:
                return False

        def rightOrder(str):
            str.replace("(", "").replace(")", "")
            return re.match("/^\d[\+\-\*\/]\d[\+\-\*\/]\d[\+\-\*\/]\d$/", str)

        # Runs when a button is pressed
        async def button_callback(interaction):
            if button_id == "⌫" and len(self.current_input) > 1:
                self.current_input = self.current_input[:-2]
            elif button_id == "=":
                current_input_math = (
                    self.current_input.replace("×", "*")
                    .replace("÷", "/")
                    .replace(" ", "")
                )
                current_input_numbers = "".join(filter(str.isdigit, current_input_math))
                if len(current_input_numbers) < 4:
                    await self.update_message_incorrect(
                        interaction, "You didn't use all the numbers!"
                    )
                elif len(current_input_numbers) > 4:
                    await self.update_message_incorrect(
                        interaction,
                        "You used too many numbers! Be sure to use 1 of each!",
                    )
                elif isBalanced(current_input_math) is False:
                    await self.update_message_incorrect(
                        interaction, "Brackets are not balanced!"
                    ) 
                elif rightOrder(current_input_math) is None:
                    await self.update_message_incorrect(
                        interaction, "Something wrong w your order miss"
                    ) 
                elif eval(current_input_math) == 24:
                    await self.update_message_correct(interaction)
                elif eval(current_input_math) != 24:
                    await self.update_message_incorrect(
                        interaction, "Sorry, that's not 24!"
                    ) 
            elif button_id != "⌫" and button_id != "=":
                # Append the button_id to the current_input
                self.current_input += button_id + " "

            await self.update_message(interaction)

        return button_callback
    
    def repeatEmbed(self, color):
        embed = discord.Embed(title = "Make 24!", color = color)

        embed.add_field(
            name="Your numbers are:",
            value=f"` {self.numbers[0]}   {self.numbers[1]}   {self.numbers[2]}   {self.numbers[3]} `",
            inline=False,
        )

        embed.add_field(
            name="Input:", value="`" + self.current_input + "`", inline=False
        )

        return embed

    async def update_message(self, interaction):
        embed = self.repeatEmbed(discord.Color.orange())

        await interaction.response.edit_message(embed=embed, view=self)

    async def update_message_correct(self, interaction):
        self.clear_items()
        embed = self.repeatEmbed(discord.Color.green())

        # TODO: fill value with winner's name (e.g., USER was the first to make 24!)
        embed.add_field(name="Congrats! You made 24!", value="", inline=False)

        await interaction.response.edit_message(embed=embed, view=self)

    async def update_message_incorrect(self, interaction, message):
        embed = self.repeatEmbed(discord.Color.red())

        embed.add_field(name="", value=message, inline=False)
        await interaction.response.edit_message(embed=embed, view=self)
    

async def setup(bot: commands.Bot):
    await bot.add_cog(TwentyFourCog(bot))
