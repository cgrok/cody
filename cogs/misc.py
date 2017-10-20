'''
MIT License

Copyright (c) 2017 Grok

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import discord
import random
import io
from discord.ext import commands
from datetime import date
from enum import Enum
from urllib.request import urlopen
from PIL import Image

halloween = date(2017, 10, 31)
christmas = date(2017, 12, 25)

class RPSLS(Enum):
    rock     = "\N{RAISED FIST}"
    paper    = "\N{RAISED HAND WITH FINGERS SPLAYED}"
    scissors = "\N{BLACK SCISSORS}"
    lizard   = "\N{LIZARD}"
    spock    = "\N{RAISED HAND WITH PART BETWEEN MIDDLE AND RING FINGERS}"


class RPSLSParser:
    def __init__(self, argument):
        argument = argument.lower()
        if argument == "rock":
            self.choice = RPSLS.rock
        elif argument == "paper":
            self.choice = RPSLS.paper
        elif argument == "scissors":
            self.choice = RPSLS.scissors
        elif argument == "lizard":
            self.choice = RPSLS.lizard
        elif argument == "spock":
            self.choice = RPSLS.spock
        else:
            raise


class Misc:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def invite(self, ctx):
        '''Official url to invite bot to your guild.'''
        inviter = discord.utils.oauth_url(self.bot.user.id, permissions=discord.Permissions(permissions=473295983))
        await ctx.send(f'Invite me to *__your__* guild with this link: \n\n<{inviter}>')

    @commands.command()
    async def reverse(self, ctx, *, msg: str = None):
        '''Writes backwards because reasons, in Embed.'''
        e = discord.Embed()
        e.colour = discord.Colour(0x8e44ad)
        if msg is None:
            usage = 'Write a message after command'
            e.description = usage
        else:
            e.description = f'\N{LEFTWARDS BLACK ARROW} `{msg.lower()[::-1]}`'
        await ctx.send(embed=e)
        await ctx.delete_message(msg)

    @commands.command(aliases=['dvwl'])
    async def devowel(self, ctx, *, text):
        '''Removes vowels from text!'''
        dvl = text.replace('a', '').replace('A', '').replace('e', '')\
                  .replace('E', '').replace('i', '').replace('I', '')\
                  .replace('o', '').replace('O', '').replace('u', '').replace('U', '')
        e = discord.Embed()
        e.color = await ctx.get_dominant_color(ctx.author.avatar_url)
        e.set_author(name=f'{ctx.author.display_name}', icon_url=ctx.author.avatar_url)
        e.description = f'\N{SMALL BLUE DIAMOND}​ ~~{text}~~\n\N{WHITE SMALL SQUARE}​ {dvl}'
        await ctx.message.delete()
        await ctx.send(embed=e)

    @commands.command(aliases=['thisis'])
    async def thisistisis(self, ctx, *, text):
        '''Replaces vowels with the letter "i", pretty useless.'''
        sis = text.replace('a', 'i').replace('A', 'I').replace('e', 'i').replace('E', 'I')\
                  .replace('o', 'i').replace('O', 'I').replace('u', 'i').replace('U', 'I')
        author = ctx.message.author
        e = discord.Embed()
        e.color = await ctx.get_dominant_color(ctx.author.avatar_url)
        e.set_author(name=f'{author.display_name}', icon_url=author.avatar_url)
        e.description = f'\N{SMALL BLUE DIAMOND}​ ~~{text}~~\n\N{WHITE SMALL SQUARE}​ {sis}'
        await ctx.message.delete()
        await ctx.send(embed=e)

    @commands.command(aliases=['christmas', 'xmas'])
    async def isitchristmas(self, ctx):
        '''Is it Christmas yet?'''
        if date.today() == christmas:
            await ctx.send("Yes, it is Christmas today.")
        else:
            msg = f'No, it is not Christmas today. There are {(christmas - date.today()).days} days until Christmas.'
            await ctx.send(msg)

    @commands.command(aliases=['halloween', 'hween', 'hwn'])
    async def isithalloween(self, ctx):
        '''Is it Halloween yet?'''
        if date.today() == halloween:
            await ctx.send("Yes, it is Halloween today.")
        else:
            msg = f'No, it is not Halloween today. There are {(halloween - date.today()).days} days until Halloween.'
            await ctx.send(msg)

    @commands.command(description='This command might get you banned', no_pm=True)
    async def spam(self, ctx, *, member=None, times: int = None):
        '''Want to annoy a member with mentions?'''

        usage = f'```Usage: {ctx.prefix}ultimate_annoying_spam_command [@member] [times]```'

        # if member or times is None:
        #     await ctx.send(usage)
        #     return

        if times is None:
            times = 25

        if times > 100:
            times = 35

        if times is 0:
            await ctx.send(f'Someone, not saying who, *cough cough {author}* felt sorry about using this command.')
            return

        if times < 0:
            await ctx.send("Well, that's just not enough times to annoy anybody. Don't chicken out now!")
            return

        await message.delete()

        for i in range(0, times):
            try:
                await ctx.send(f'{member.mention} LOL')
            except Exception:
                await ctx.send(usage)

    @commands.command(aliases=['tinyurl'])
    async def tiny_url(self, ctx, str = None):
        '''Shorten URL'''
        tinyurl = urlopen("http://tinyurl.com/api-create.php?url=" + str).read().decode("utf-8")
        usage = f'Usage: {ctx.prefix}tinyurl https://github.com/verixx/grokbot'
        url = ctx.message.starts_with('https://')
        if str is None:
            await ctx.send(usage)
        if str is int:
            await ctx.send(usage)
        if str is url:
            await ctx.send(tinyurl)
        else:
            pass

    @commands.command(aliases=['qr','qrgen'])
    async def generateqr(self, ctx, *, str = None):
        '''Generate a QR code'''
        if str == None:
            await ctx.send(f"You must include text or a link to convert to a QR code, {ctx.message.author.mention}")
        else:
            url = f'https://chart.googleapis.com/chart?chs=300x300&cht=qr&chl={str}&choe=UTF-8'
            with urlopen(url) as link:

                qrimg = io.BytesIO(link.read())
                #qrimg = Image.open(qrimgpage)
            await ctx.send(file=qrimg)

    @commands.command(aliases=['rock', 'paper', 'scissors', 'lizard', 'spock', 'rps'])
    async def settle(self, ctx, your_choice : RPSLSParser= None):
        '''Play rock paper scissors lizard spock '''
        if your_choice != None:
            author = ctx.message.author.display_name
            grok = self.bot.user.name
            player_choice = your_choice.choice
            available = RPSLS.rock, RPSLS.paper, RPSLS.scissors, RPSLS.lizard, RPSLS.spock
            bot_choice = random.choice((available))
            cond = {
                    (RPSLS.rock,     RPSLS.paper)    : False,
                    (RPSLS.rock,     RPSLS.scissors) : True,
                    (RPSLS.rock,     RPSLS.lizard)   : True,
                    (RPSLS.rock,     RPSLS.spock)    : False,
                    (RPSLS.paper,    RPSLS.rock)     : True,
                    (RPSLS.paper,    RPSLS.scissors) : False,
                    (RPSLS.paper,    RPSLS.lizard)   : False,
                    (RPSLS.paper,    RPSLS.spock)    : True,
                    (RPSLS.scissors, RPSLS.rock)     : False,
                    (RPSLS.scissors, RPSLS.paper)    : True,
                    (RPSLS.scissors, RPSLS.lizard)   : True,
                    (RPSLS.scissors, RPSLS.spock)    : False,
                    (RPSLS.lizard,   RPSLS.rock)     : False,
                    (RPSLS.lizard,   RPSLS.paper)    : True,
                    (RPSLS.lizard,   RPSLS.scissors) : False,
                    (RPSLS.lizard,   RPSLS.spock)    : True,
                    (RPSLS.spock,    RPSLS.rock)     : True,
                    (RPSLS.spock,    RPSLS.paper)    : False,
                    (RPSLS.spock,    RPSLS.scissors) : True,
                    (RPSLS.spock,    RPSLS.lizard)   : False
                   }
            em = discord.Embed()
            em.color = await ctx.get_dominant_color(ctx.author.avatar_url)
            em.add_field(name=f'{author}', value=f'{player_choice.value}', inline=True)
            em.add_field(name=f'{grok}', value=f'{bot_choice.value}', inline=True)
            if bot_choice == player_choice:
                outcome = None
            else:
                outcome = cond[(player_choice, bot_choice)]
            if outcome is True:
                em.set_footer(text="You win!")
                await ctx.send(embed=em)
            elif outcome is False:
                em.set_footer(text="You lose...")
                await ctx.send(embed=em)
            else:
                em.set_footer(text="We're square")
                await ctx.send(embed=em)
        else:
            msg = 'rock, paper, scissors, lizard, OR spock'
            await ctx.send(f'Enter: `{ctx.prefix}{ctx.invoked_with} {msg}`', delete_after=5)


def setup(bot):
    return bot.add_cog(Misc(bot))
