import discord
from discord.ext import commands
from cogs.utils.dataIO import dataIO
from collections import namedtuple, defaultdict, deque
from datetime import datetime
from copy import deepcopy
from .utils import checks
from cogs.utils.chat_formatting import pagify, box
from enum import Enum
from __main__ import send_cmd_help
from discord.ext import commands
import time
import re
import os
from datetime import datetime, timedelta


def paginate_string(content):
    page = '```'
    pages = []
    for item in content:
        if len(page + '\n' + item) > 1997:
            page = page + '```'
            pages.append(page)
            page = '```'
        page = page + '\n' + item
    page = page + '```'
    pages.append(page)
    return pages

def get_size(start_path = '.'):
    return sum(os.path.getsize(os.path.join(dirpath,filename)) for dirpath, dirnames, filenames in os.walk(start_path) for filename in filenames)

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
    @checks.serverowner_or_permissions(administrator=True)
    async def list(self, ctx, server_id_or_substring=None):
        """"""
        

def setup(bot):
    bot.add_cog(StringFuncs(bot))
