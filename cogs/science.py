else if
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

    @commands.command(pass_context=True)
    async def test(self, ctx):
        server = ctx.message.server
        servers = []
        for server in self.bot.servers:
            servers.append(server.name)
            print(str(server))

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

    @commands.group(name="file", pass_context=True)
    async def _file(self, ctx):
        """Logged file operations"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @_file.command(pass_context=True)
    @checks.serverowner_or_permissions(administrator=True)
    async def list(self, ctx, serverid=None):
        """List names of all logged file attachments for the specified server. Default is the current server if no other server is specified. """
        if not serverid:
            serverid = ctx.message.server.id
        server = self.bot.get_server(serverid)
        # print('Server: ' + str(server.name))
        # print('Server ID: ' + str(server.id))
        await self.bot.say('These are all the logged attachments for ' + str(server.name) + ' (Server ID: ' + str(server.id) + ')')
        B = ['.log', '.json']
        blacklist = re.compile('|'.join([re.escape(word) for word in B]))
        files_ = []
        for path, subdirs, filelist in os.walk("/home/red/Red-DiscordBot/data/activitylogger/" + str(server.id)):
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

    @_file.command(pass_context=True)
    @checks.serverowner_or_permissions(administrator=True)
    async def info(self, ctx, server_id_or_substring=0):
        """Show info about logged file attachments. If no server is specified, info is given for all servers."""
        if server_id_or_substring == 0:
            servers = []
            for server in self.bot.servers:
                servers.append(server)
        elif type(server_id_or_substring) is string:
            myservers = []
            for server in self.bot.servers:
                myservers.append(server)
            servers = [server for server in myservers if server_id_or_substring in str(server)]
        elif type(server_id_or_substring) is int and len(server_id_or_substring) is 18:
            myservers = []
            for server in self.bot.servers:
                myservers.append(server)
            servers = [server for server in myservers if server_id_or_substring in server.id]
        else:
            # await send_cmd_help(ctx)
            await self.bot.say('Error: optional server argument must be either a partial name of a server or a server id.')
        print(servers)
        B = ['.log', '.json']
        blacklist = re.compile('|'.join([re.escape(word) for word in B]))

        totalfilecount = 0
        totalimagefilecount = 0
        totalfilesize = 0
        filecounts = []
        imagefilecounts = []
        filesizes = []

        for server in servers:
            files_ = []
            for path, subdirs, filelist in os.walk("/home/red/Red-DiscordBot/data/activitylogger/" + server.id):
                for file in filelist:
                    files_.append(str(file))
            files = [word for word in files_ if not blacklist.search(word)]
            imageextensions = ['.png', '.jpg', 'jpeg', '.gif']
            imagefiles = []
            for filename in files:
                for ext in imageextensions:
                    if filename.endswith(ext):
                        imagefiles.append(filename)
            totalfilecount += len(files)
            totalimagefilecount += len(imagefiles)
            totalfilesize += get_size("/home/red/Red-DiscordBot/data/activitylogger/" + server.id)
            filecounts.append(str(len(files)))
            imagefilecounts.append(str(len(imagefiles)))
            filesizes.append(str(round(get_size("/home/red/Red-DiscordBot/data/activitylogger/" + server.id)/1000000, 3)) + ' MB')

        await self.bot.say('File Info:')
        lines = []
        i = 0
        for server in servers:
            lines.append(str(server.name) + ':\n  File Count:   ' + str(filecounts[i]) + '\n  Image Files:  ' + str(imagefilecounts[i]) + '\n  Total Size:   ' + str(filesizes[i]) + '\n')
            i += 1
        lines.append('Total:\n  File Count:   ' + str(totalfilecount) + '\n  Image Files:  ' + str(totalimagefilecount) + '\n  Total Size:   ' + str(round(totalfilesize/1000000, 3)) + 'MB')
        pages = paginate_string(lines)
        for page in pages:
            await self.bot.say(page)
            # This pause reduces the choppyness of the messages by going as fast as Discord allows but at regular intervals
            time.sleep(1)

def setup(bot):
    bot.add_cog(SCIENCE(bot))
