"""
Contains the HelpCog class.

author: Muhammad Nabil (myn55)
version: 9/16/2023
"""

# TODO: take in option argument so help command can display information about a specific command or category

import discord
from discord.commands import slash_command
from .base_cog import ResumeCog

class HelpCog(ResumeCog):
    """
    Contains the bot's dedicated help command.
    """

    @slash_command(name="help", description="Sends an embed containing all commands of the bot and their purposes.", guilds=[])
    async def help(self, ctx : discord.ApplicationContext,
                   args : discord.Option(discord.SlashCommandOptionType.string, name="option", description="The command or category to display.",
                                         required=False, default=None)) -> None:
        """
        Sends an embed containing every caterogry and command registered in the bot.
        """
        helpEmbed = discord.Embed(title="Resume Checker Help Menu", color=discord.Color.from_rgb(255, 255, 255))

        cogList = ctx.bot.cogs
        categoryNames = [x[0:len(x)-3] for x in cogList.keys()]
        commandList = ctx.bot.application_commands
        commandNames = [x.name for x in commandList]

        helpEmbed.add_field(
            name="List of categories:",
            value=', '.join(categoryNames),
            inline=False
        )

        helpEmbed.add_field(
            name="List of commands:",
            value=', '.join(commandNames),
            inline=False
        )

        await ctx.respond(embed=helpEmbed)