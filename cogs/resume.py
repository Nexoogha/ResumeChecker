"""
Contains the ResumeCog class.

author: Omer Ahmed (omerahmed05), Jonathan Woodbury (jonathanw22), Muhammad Nabil (myn55)
version: 09/16/2023
"""

import discord, nltk
from discord.commands import slash_command
from nltk.corpus import stopwords
from .base_cog import CCog
from pypdf import PdfReader
from datetime import datetime

def extract_key_terms(text : str):
    tokens = nltk.word_tokenize()

class ResumeCog(CCog):
    """
    Contains the main functions of the bot such as parsing resumes.
    """

    @slash_command(name="readresume", description="Reads a PDF attachment file.", guilds=[1152451000079220897])
    async def read(self, ctx : discord.ApplicationContext,
                   resume : discord.Option(discord.SlashCommandOptionType.attachment,
                                           name="resume",
                                           description="The resume to scan (PDF format)"),
                    verbose : discord.Option(discord.SlashCommandOptionType.boolean,
                                             name="verbose",
                                             description="Whether to display extra PDF information or not.",
                                             default = False)):
        """
        Interprets the text of the attached PDF file along with its metadata.
        Debugging command.
        """

        # Check if it is a PDF file
        url = resume.url
        if not url.endswith('pdf'):
            await ctx.respond(content="The file you provided is not a PDF.", ephemeral=True)
            return
        
        await ctx.respond("Reading PDF...")

        content = await resume.read()

        # Write the PDF
        with open('metadata.pdf', 'wb') as pdf:
            pdf.write(content)
        
        with open('metadata.pdf', 'rb') as pdf:
            reader = PdfReader(pdf)
            md = reader.metadata

            # Send verbose info
            if verbose:
                infoEmbed = discord.Embed(title=resume.filename)
                infoEmbed.set_author(name=(md.author or 'Unknown author'))

                infoEmbed.add_field(
                    name="Title",
                    value=(md.title or 'None'),
                    inline=False
                )

                infoEmbed.add_field(
                    name="Creator",
                    value=(md.creator or 'Not specified')
                )

                infoEmbed.add_field(
                    name="Producer",
                    value=(md.producer or 'Not specified')
                )

                infoEmbed.add_field(
                    name="Creation Date",
                    value=str(md.creation_date or 'Not specified'),
                    inline=False
                )

                await ctx.channel.send(embed=infoEmbed)
            
            # Parse text
            for i in range(len(reader.pages)):
                page = reader.pages[i]
                text = page.extract_text()
                await ctx.channel.send(f'Text excerpt from page {i+1}: ```{text[0:1920]}```')