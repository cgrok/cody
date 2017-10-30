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
    rock     = "\N{RAISED FIST} Rock!"
    paper    = "\N{RAISED HAND WITH FINGERS SPLAYED} Paper!"
    scissors = "\N{BLACK SCISSORS} Scissors!"
    lizard   = "\N{LIZARD} Lizard!"
    spock    = "\N{RAISED HAND WITH PART BETWEEN MIDDLE AND RING FINGERS} Spock!"


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

    @commands.command()
    async def textmojify(self, ctx, *, msg):
        """Convert text into emojis"""
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass

        if msg != None:
            msg = text.lower().replace(' ', '    ').replace('10', ':keycap_ten:').replace('ab', ':ab:').replace('cl', ':cl:').replace('0', ':zero:').replace('1', ':one:').replace('2', ':two:').replace('3', ':three:').replace('4', ':four:').replace('5', ':five:').replace('6', ':six:').replace('7', ':seven:').replace('8', ':eight:').replace('9', ':nine:').replace('!', ':exclamation:').replace('?', ':grey_question:').replace('vs', ':vs:').replace('.', ':small_orange_diamond:').replace(',', ':small_red_triangle_down:').replace('a', ':a:').replace('b', ':b:').replace('c', ':regional_indicator_c:').replace('d', ':regional_indicator_d:').replace('e', ':regional_indicator_e:').replace('f', ':regional_indicator_f:').replace('g', ':regional_indicator_g:').replace('h', ':regional_indicator_h:').replace('i', ':regional_indicator_i:').replace('j', ':regional_indicator_j:').replace('k', ':regional_indicator_k:').replace('l', ':regional_indicator_l:').replace('m', ':regional_indicator_m:').replace('n', ':regional_indicator_n:').replace('o', ':o2:').replace('p', ':parking:').replace('q', ':regional_indicator_q:').replace('r', ':regional_indicator_r:').replace('s', ':regional_indicator_s:').replace('t', ':regional_indicator_t:').replace('u', ':regional_indicator_u:').replace('v', ':regional_indicator_v:').replace('w', ':regional_indicator_w:').replace('x', ':regional_indicator_x:').replace('y', ':regional_indicator_y:').replace('z', ':regional_indicator_z:')
            await ctx.send(text)
        else:
            await ctx.send('Write something, reee!', delete_after=3.0)

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


    @commands.command(aliases=['tinyurl'])
    async def tiny_url(self, ctx, str = None):
        '''Shorten URL'''
        usage = f'**Usage:**\n`{ctx.prefix}{ctx.invoked_with} https://cdn.discordapp.com/avatars/323578534763298816/a_e9ce069bedf43001b27805cd8ef9c0db.gif`'
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass

        if url != None:
            apitiny = 'http://tinyurl.com/api-create.php?url='
            tiny_url = urlopen(apitiny + link).read().decode("utf-8")
            e = discord.Embed()
            e.color = await ctx.get_dominant_color(ctx.author.avatar_url)
            e.add_field(name="🌏 Original", value=f'~~`{link}`~~')
            e.add_field(name="Tinyurl 🔗", value=f'```{tiny_url}```')
            try:
                await ctx.send(embed=e)
            except discord.HTTPException:
                em_list = await embedtobox.etb(e)
                for page in em_list:
                    await ctx.send(page)

        else:
            await ctx.send(usage, delete_after=15)
            return

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
        '''Play rock paper scissors, lizard spock '''
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

    @commands.command()
    async def guess(self, number: int):
        """Write a number between 1 and 7"""
        answer = random.randint(1, 7)

        e = discord.Embed()
        e.colour = discord.Colour(0x9b59b6)
        if number < answer or number > answer:
            q_mark = '\N{BLACK QUESTION MARK ORNAMENT}'
            guessed_wrong = [
                'Not even close, the right number was:',
                'Better luck next time, the number was:',
                'How could you have known that the number was:',
                'Hmm, well, the right number was:',
                'Not getting any better, the number was:',
                'Right number was:'
                ]
            e.add_field(name=f'{q_mark} Choice: `{number}`', 
                        value=f'```{random.choice(guessed_wrong)} {answer}```', inline=True)
            try:
                await ctx.send(embed=e)
            except discord.HTTPException:
                em_list = await embedtobox.etb(e)
                for page in em_list:
                    await ctx.send(page)

        if number is answer:
            q_mark = '\N{BLACK QUESTION MARK ORNAMENT}'
            guessed_right = [
                'You guessed correctly!',
                'Everyone knew you could do it!',
                'You got the right answer!',
                'History will remember you...'
                ]
            e.add_field(name=f'{q_mark} Correct number: `{answer}`', 
                        value=f'```{random.choice(guessed_right)}```', inline=True)
            try:
                await ctx.send(embed=e)
            except discord.HTTPException:
                em_list = await embedtobox.etb(e)
                for page in em_list:
                    await ctx.send(page)
        else:
            return


def setup(bot):
    return bot.add_cog(Misc(bot))
