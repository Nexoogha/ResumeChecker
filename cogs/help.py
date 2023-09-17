"""
Contains the HelpCog class.

author: Muhammad Nabil (myn55)
version: 09/16/2023
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
        help_embed = discord.Embed(title="Resume Checker Help Menu", color=discord.Color.from_rgb(255, 255, 255))

        command_list = ctx.bot.application_commands
        command_names = [x.name for x in command_list]

        # No argument passed, list commands
        if not arg:
            help_embed.add_field(
                name="List of commands:",
                value=', '.join(command_names),
                inline=False
            )

            help_embed.add_field(
                name="Extra",
                value="Use `/help <command name>` to get more information about a command.",
                inline=False
            )
        
        # Argument passed, find command and display info
        else:
            if arg in command_names:
                help_embed.add_field(
                    name=arg,
                    value=ctx.bot.get_command(arg).description
                )
            else:
                await ctx.respond(content=f"Could not find {arg}", ephemeral=True)
                return

        await ctx.respond(embed=help_embed)