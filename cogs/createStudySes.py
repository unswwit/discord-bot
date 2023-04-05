import discord
from discord.ext import commands
from discord.ui import Button
import random_topic

class MyView(discord.ui.View):
    def __init__(self, author_id):
        super().__init__()
        self.going_users = set([author_id])

        self.add_item(Button(style=discord.ButtonStyle.green, label="Going", custom_id="going"))
        self.add_item(Button(style=discord.ButtonStyle.red, label="Not Going", custom_id="not_going"))
        self.author_id = author_id 

        self.attendees_label = discord.utils.get(self.children, id="attendees_label")
        #this allows the the bot to know which button was clicked so it can respond appropriately 
        if not self.attendees_label:
            self.attendees_label = discord.ui.Button(label="Attendees:", disabled=True, id="attendees_label")
            self.add_item(self.attendees_label)
        
        self.attendees_list = discord.utils.get(self.children, id="attendees_list")
        if not self.attendees_list:
            self.attendees_list = discord.ui.Button(label="", disabled=True, id="attendees_list")
            self.add_item(self.attendees_list)

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id == self.author_id:
            return True
        await interaction.response.send_message("Only the command author can interact with this message.", ephemeral=True)
        return False

    async def on_button_click(self, button: discord.ui.Button, interaction: discord.Interaction):
        if button.custom_id == "going":
            self.going_users.add(interaction.user.id)
        elif button.custom_id == "not_going":
            if interaction.user.id in self.going_users:
                self.going_users.remove(interaction.user.id)

        going_usernames = [f"<@{user_id}>" for user_id in self.going_users]
        self.attendees_list.label = "\n".join(going_usernames)

class Buttons(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test_buttons(self, ctx):
        view = MyView(ctx.author.id)
        await ctx.send("Are you going or not?", view=view) 


async def setup(bot):
    bot.add_cog(Buttons(bot))

#the bot will be triggered by the slash 
bot = commands.Bot(command_prefix='/')

#user types /random_topic and the command will be executed 
@bot.command(name='random-topic')
async def random_topic_command(ctx):
    #generates a random topic from random_topic mudule and saves it to a variable called topic
    topic = random_topic.get_random_topic()
    #creates a string called message allowing variables to be included 
    message = f"Conversation topic: {topic}"
    await ctx.send(message)

