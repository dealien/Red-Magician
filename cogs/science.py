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

try: # Check if BeautifulSoup4 is installed
    from bs4 import BeautifulSoup
    soupAvailable = True
except:
    soupAvailable = False
import aiohttp
import browser_cookie3

def setup(bot):
    if soupAvailable:
        bot.add_cog(SCIENCE(bot))
    else:
        raise RuntimeError("You need to run `pip3 install beautifulsoup4`")

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

class SCIENCE:
    """A custom cog that does stuff! Lots of stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def punch(self, user : discord.Member):
        """I will puch anyone! >.<"""

        # Command function
        await self.bot.say("ONE PUNCH! And " + user.mention + " is out! ლ(ಠ益ಠლ)")
    
    # @commands.command()
    # async def dotanow(self):
    #     """How many players are online atm?"""

    #     # Command function
    #     url = "https://steamdb.info/app/570/graphs/" #build the web adress
    #     async with aiohttp.get(url) as response:
    #         soupObject = BeautifulSoup(await response.text(), "html.parser")
    #     try:
    #         online = soupObject.find(class_='home-stats').find('li').find('strong').get_text()
    #         await self.bot.say(online + ' players are playing this game at the moment')
    #     except:
    #         await self.bot.say("Couldn't load amount of players. No one is playing this game anymore or there's an error.")

    @commands.group(name="files", pass_context=True)
    async def _files(self, ctx):
        """Logged file operations"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @_files.command(pass_context=True)
    @checks.serverowner_or_permissions(administrator=True)
    async def list(self, ctx, server=None):
        """List names of all logged file attachments for the specified server."""
        if not server:
            server = ctx.message.server.id
            servername = ctx.message.server
            await self.bot.say('These are all the logged attachments for ' + str(servername) + ' (Server ID: ' + str(server) + ')')
        else:
            await self.bot.say('These are all the logged attachments for ' + str(server))
        B = ['.log', '.json']
        blacklist = re.compile('|'.join([re.escape(word) for word in B]))
        files_ = []
        for path, subdirs, filelist in os.walk("/home/red/Red-DiscordBot/data/activitylogger/" + server):
            for file in filelist:
                files_.append(str(file))
        ifiles = [word for word in files_ if not blacklist.search(word)]
        files = []
        for item in ifiles:
            indexid = item[:18]
            filename = item[19:]
            files.append(indexid + "   " + filename)
        await self.bot.say('Number of files: ' + str(len(files)))
        pages = paginate_string(files)
        await self.bot.say('Number of pages: ' + str(len(pages)))
        for page in pages:
            await self.bot.say(page)
            # This pause reduces the choppyness of the messages by going as fast as Discord allows but at regular intervals
            time.sleep(1)

    @_files.command(pass_context=True)
    async def info(self, ctx):
        """Show info about logged file attachments for the current server."""
        server = ctx.message.server.id
        servername = ctx.message.server
        B = ['.log', '.json']
        blacklist = re.compile('|'.join([re.escape(word) for word in B]))
        files_ = []
        for path, subdirs, filelist in os.walk("/home/red/Red-DiscordBot/data/activitylogger/" + server):
            for file in filelist:
                files_.append(str(file))
        files = [word for word in files_ if not blacklist.search(word)]
        imageextensions = ['.png', '.jpg', 'jpeg', '.gif']
        imagefiles = []
        for filename in files:
            for ext in imageextensions:
                if filename.endswith(ext):
                    imagefiles.append(filename)

        message=discord.Embed(title=str(servername), color=0x000000)
        message.add_field(name="Files", value=str(len(files)), inline=True)
        message.add_field(name="Total Size", value=str(get_size("/home/red/Red-DiscordBot/data/activitylogger/" + server)) + " Bytes", inline=True)
        message.add_field(name="Images", value=str(len(imagefiles)), inline=False)
        message.set_footer(text=str(datetime.now()))
        await self.bot.say(embed=message)

def setup(bot):
    bot.add_cog(SCIENCE(bot))