import time
import re
import discord
from discord.ext import commands
import os

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

class SCIENCE:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mycom(self):
        """This does stuff!"""

        # Command function
        await self.bot.say("I can do stuff!")

    @commands.command()
    async def punch(self, user : discord.Member):
        """I will puch anyone! >.<"""

        # Command function
        await self.bot.say("ONE PUNCH! And " + user.mention + " is out! ლ(ಠ益ಠლ)")
    
    @commands.command()
    async def dotanow(self):
        """How many players are online atm?"""

        # Command function
        url = "https://steamdb.info/app/570/graphs/" #build the web adress
        async with aiohttp.get(url) as response:
            soupObject = BeautifulSoup(await response.text(), "html.parser")
        try:
            online = soupObject.find(class_='home-stats').find('li').find('strong').get_text()
            await self.bot.say(online + ' players are playing this game at the moment')
        except:
            await self.bot.say("Couldn't load amount of players. No one is playing this game anymore or there's an error.")

    @commands.command()
    async def listfiles(self):
        """List all logged file attachments from activitylogger."""

        # Command function
        await self.bot.say('These are all the logged attachments...')
        B = ['.log', '.json']
        blacklist = re.compile('|'.join([re.escape(word) for word in B]))
        files_ = []
        for path, subdirs, filelist in os.walk("/home/red/Red-DiscordBot/data/activitylogger/"):
            for file in filelist:
                files_.append(str(file))
        files = [word for word in files_ if not blacklist.search(word)]
        await self.bot.say('Number of files: ' + str(len(files)))
        pages = paginate_string(files)
        for page in pages:
            await self.bot.say(page)
            # This pause reduces the choppyness of the messages by going as fast as Discord allows but at regular intervals
            time.sleep(0.9)

    @commands.command()
    async def filemenu(self):
        """List all logged file attachments from activitylogger. 

        This one is in an interactive menu format."""

        # Command function
        await self.bot.say('These are all the logged attachments...')
        B = ['.log', '.json']
        blacklist = re.compile('|'.join([re.escape(word) for word in B]))
        files_ = []
        for path, subdirs, filelist in os.walk("/home/red/Red-DiscordBot/data/activitylogger/"):
            for file in filelist:
                files_.append(str(file))
        files = [word for word in files_ if not blacklist.search(word)]
        await self.bot.say('Number of files: ' + str(len(files)))
        pages = paginate_string(files)

def setup(bot):
    bot.add_cog(SCIENCE(bot))