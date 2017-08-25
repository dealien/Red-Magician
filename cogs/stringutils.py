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


class StringFuncs:
    """A cog that provides various string analysis and manipulation commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="string", pass_context=True)
    async def _string(self, ctx):
        """Logged file operations"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @_file.command(pass_context=True)
    async def length(self, ctx, input_string):
        """Returns the length of the input string."""
        await self.bot.say(str(len(input_string)))
        

def setup(bot):
    bot.add_cog(StringFuncs(bot))

pagify()