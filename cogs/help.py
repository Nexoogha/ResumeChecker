"""
Contains the HelpCog class.

author: Muhammad Nabil (myn55)
version: 9/16/2023
"""

import discord
from discord.commands import slash_command
from .base_cog import CCog

class HelpCog(CCog):
    """
    Contains the bot's dedicated help command.
    """

    @slash_command(name="help", description="Sends an embed containing all commands of the bot and their purposes.", guilds=[])
    async def help(self, ctx : discord.ApplicationContext,
                   arg : discord.Option(discord.SlashCommandOptionType.string, name="option",
                                         description="The command to display information abour.",
                                         required=False, default=None)) -> None:
        """
        Sends an embed containing every caterogry and command registered in the bot.
        """
        helpEmbed = discord.Embed(title="Resume Checker Help Menu", color=discord.Color.from_rgb(255, 255, 255))

        cogList = ctx.bot.cogs
        categoryNames = [x[0:len(x)-3] for x in cogList.keys()]
        commandList = ctx.bot.application_commands
        commandNames = [x.name for x in commandList]

        # No argument passed, list commands
        if not arg:
            helpEmbed.add_field(
                name="List of commands:",
                value=', '.join(commandNames),
                inline=False
            )

            helpEmbed.add_field(
                name="Extra",
                value="Use `/help <command name>` to get more information about a command.",
                inline=False
            )
        
        # Argument passed, find command and display info
        else:
            if arg in commandNames:
                helpEmbed.add_field(
                    name=arg,
                    value=ctx.bot.get_command(arg).description
                )
            else:
                await ctx.respond(content=f"Could not find {arg}", ephemeral=True)

        await ctx.respond(embed=helpEmbed)