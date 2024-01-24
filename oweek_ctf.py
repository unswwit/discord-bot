import discord
import random

WINNING_NUM = 7
MAX_RANDOM = 10

async def run_ctf(user):
    # Generate a random number between 1 and 10
    random_number = random.randint(1, MAX_RANDOM)

    # Hardcoded winning number
    winning_number = WINNING_NUM

    if random_number == winning_number:
        # If the generated number matches the winning number, send a DM to the user
        await user.send(f"Congratulations, {user.name} 🧡! Please present this flag to the WIT stall to claim your prize: \n" + "`${WIT_FLAG_2023: Yay thank you for helping Willow by exploring the server!}`")