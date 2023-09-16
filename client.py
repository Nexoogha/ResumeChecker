import discord, json
from colorama import init, Fore, Back, Style
init()

class ResumeBot(discord.Client):
    async def on_ready(self):
        print(Fore.GREEN+f"Successfully logged in as {Fore.CYAN+Style.BRIGHT+str(self.user)}"+Style.RESET_ALL)

client = ResumeBot()
with open("config.json", "r") as config:
    client.run(json.load(config)["token"])