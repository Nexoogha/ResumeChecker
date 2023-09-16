"""
Contains the custom CCog Cog subclass.

author: Muhammad Nabil (myn55)
version: 9/16/2023
"""

import discord
from colorama import Fore, Style

class CCog(discord.Cog):
    """
    Custom Cog subclass for the bot for load success notification.
    """
    def __init__(self) -> None:
        print(Fore.BLUE+f"{self.__class__.__name__} "+Fore.GREEN+"sucessfully loaded!"+Style.RESET_ALL)