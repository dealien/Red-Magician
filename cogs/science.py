import discord
from discord.ext import commands
from collections import defaultdict, deque 
from cogs.utils.chat_formatting import pagify, box
from __main__ import send_cmd_help
import os

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

class Science:
    """A custom cog that does stuff! Lots of stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def test(self, ctx):
        server = ctx.message.server
        servers = []
        for server in self.bot.servers:
            servers.append(server.name)
            print(str(server))

    @commands.command()
    async def punch(self, user : discord.Member):
        """I will punch anyone! >.<"""

        # Command function
        await self.bot.say("ONE PUNCH! And " + user.mention + " is out! ლ(ಠ益ಠლ)")

def setup(bot):
    bot.add_cog(Science(bot))
