import discord
from discord.ext import commands
from collections import namedtuple, defaultdict, deque
from copy import deepcopy
from .utils import checks
from cogs.utils.chat_formatting import pagify, box
from enum import Enum
from __main__ import send_cmd_help
from discord.ext import commands
import re


class StringUtilities:
    """A cog that provides various string analysis and manipulation commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="string", pass_context=True)
    async def _string(self, ctx):
        """Various string manipulations"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @_string.command(pass_context=True)
    async def length(self, ctx, input_string):
        """Returns the length of the input string."""
        await self.bot.say('`' + str(len(input_string)) + '`')

    @_string.command(pass_context=True)
    async def reverse(self, ctx, input_string):
        """Returns the input string backwards."""
        reverse = ''
        for i in input_string:
            reverse = i + reverse
        await self.bot.say('`' + reverse + '`')


def setup(bot):
    bot.add_cog(StringUtilities(bot))
