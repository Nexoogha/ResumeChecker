"""
Contains the MaintenanceCog class.

author: Muhammad Nabil (myn55)
version: 9/16/2023
"""

import discord
from discord.commands import slash_command
from .base_cog import ResumeCog

class MaintenanceCog(ResumeCog):
    """
    Contains commands for maintaining and checking the status of the bot.
    """

    @slash_command(name="ping", description="Returns the API latency of the bot in milliseconds.", guilds=[])
    async def ping(self, ctx : discord.ApplicationContext) -> None:
        """
        Checks the API latency of the bot and sends it in milliseconds.
        """
        latency = int(ctx.bot.latency * 1000)
        await ctx.respond(f"Client latency is {latency}ms, {'not too bad!' if latency < 300 else 'not great.'}")