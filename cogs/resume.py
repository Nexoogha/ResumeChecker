"""
Contains the ResumeCog class.

author: Muhammad Nabil (myn55)
version: 9/16/2023
"""

import discord
from discord.commands import slash_command
from .base_cog import CCog

class ResumeCog(CCog):
    """
    Contains the main functions of the bot from parsing resumes and claculating eligibility for the job.
    """