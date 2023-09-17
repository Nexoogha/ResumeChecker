"""
Contains the ResumeCog class.

author: Omer Ahmed (omerahmed05), Jonathan Woodbury (jonathanw22), Muhammad Nabil (myn55)
version: 09/16/2023
"""

import discord
from discord.commands import slash_command
from .base_cog import CCog
from pypdf import PdfReader
import requests

class ResumeCog(CCog):
    """
    Contains the main functions of the bot from parsing resumes and claculating eligibility for the job.
    """

    @slash_command(name="readresume", description="Takes in a resume attachment file.", guilds=[])
    async def read(self, ctx : discord.ApplicationContext,
                   resume : discord.Option(discord.SlashCommandOptionType.attachment, name="resume",
                                           description="The resume to scan (PDF format)")):
        
        # Check if it is a PDF file
        url = resume.url
        if not url.endswith('pdf'):
            await ctx.respond(content="The file you provided is not a PDF.", ephemeral=True)
            return
        
        await ctx.respond("Reading PDF...")

        content = await resume.read()

        reader = PdfReader(content)