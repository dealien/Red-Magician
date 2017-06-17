from cogs.utils.dataIO import dataIO
from discord.ext import commands
import os
import random
import asyncio


class RPSLS:
    """Play Rock Paper Scissors Lizard Spock."""

    def __init__(self, bot):
        self.bot = bot
        self.weaknesses = dataIO.load_json('data/rpsls/weaknesses.json')

    @commands.command()
    async def rpsls(self, choice: str):
        """Play Rock Paper Scissors Lizard Spock by Sam Kass in Discord! Rules:\nScissors cuts Paper\nPaper covers Rock\nRock crushes Lizard\nLizard poisons Spock\nSpock smashes Scissors\nScissors decapitates Lizard\nLizard eats Paper\nPaper disproves Spock\nSpock vaporizes Rock\nAnd as it has always Rock crushes Scissors"""
        check = True
        playerchoice = choice.lower()
        if playerchoice == 'rock':
            playeremote = ':moyai:'
        elif playerchoice == 'spock':
            playeremote = ':vulcan:'
        elif playerchoice == 'paper':
            playeremote = ':page_facing_up:'
        elif playerchoice in ['scissors', 'lizard']:
            playeremote = ':{}:'.format(playerchoice)
        else:
            await self.bot.say('Invalid choice.')
            check = False
        if check:
            botchoice = random.choice(['rock', 'paper', 'scissors', 'lizard', 'spock'])
            if botchoice == 'rock':
                botemote = ':moyai:'
            elif botchoice == 'spock':
                botemote = ':vulcan:'
            elif botchoice == 'paper':
                botemote = ':page_facing_up:'
            else:
                botemote = ':{}:'.format(botchoice)
            await self.bot.say('{} vs. {}, who will win?'.format(playeremote, botemote))
            await asyncio.sleep(2)
            if playerchoice in self.weaknesses[botchoice]:
                await self.bot.say('You win! :sob:')
            elif botchoice in self.weaknesses[playerchoice]:
                await self.bot.say('I win! :smile:')
            else:
                await self.bot.say('It\'s a draw! :neutral_face:')


def check_folder():
    if not os.path.exists('data/rpsls'):
        print('Creating data/rpsls folder...')
        os.makedirs('data/rpsls')


def setup(bot):
    check_folder()
    bot.add_cog(RPSLS(bot))
