"""
Main driver code for the Discord bot.

author: Muhammad Nabil (myn55)
version: 9/16/2023
"""

import discord, json
from cogs.maintenance import MaintenanceCog
from cogs.help import HelpCog
from colorama import init, Fore, Back, Style
init()

class ResumeBot(discord.Bot):
    def __init__(self, description=None, *args, **options) -> None:
        super().__init__(description, *args, **options)

    async def on_ready(self) -> None:
        print(Fore.GREEN+f"Successfully logged in as {Fore.CYAN+Style.BRIGHT+str(self.user)}"+Style.RESET_ALL)

    async def on_message(self, msg : discord.Message) -> None:
        print(msg.content)

# Set up intents for our bot in order to have permission to access members and message content
intents = discord.Intents()
intents.members = True
intents.guild_messages = True
intents.message_content = True

client = ResumeBot(intents=intents)
with open("config.json", "r") as config:
    client.add_cog(MaintenanceCog())
    client.add_cog(HelpCog())

    client.run(json.load(config)["token"])