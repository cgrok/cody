import discord
from discord.ext import commands
from datetime import date
from urllib.request import urlopen

halloween = date(2017, 10, 31)
christmas = date(2017, 12, 25)


class Misc:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['install'])
    async def invite(self, ctx):
        """Official url to invite bot to your server."""
        inviter = discord.utils.oauth_url(self.bot.user.id, permissions=discord.Permissions(permissions=473295983))
        await ctx.channel.send(f'Invite me to *__your__* server with this link: \n\n<{inviter}>')

    @commands.command()
    async def reverse(self, ctx, *, msg: str = None):
        """Writes backwards because reasons, in Embed"""
        e = discord.Embed()
        e.colour = discord.Colour(0x8e44ad)
        if msg is None:
            usage = 'Write a message after command'
            e.description = usage
        else:
            e.description = f'\N{LEFTWARDS BLACK ARROW} `{msg.lower()[::-1]}`'
        await ctx.channel.send(embed=e)
        await ctx.delete_message(msg)

    @commands.command(aliases=['dvwl'])
    async def devowel(self, ctx, *text):
        dvl = text.replace('a', '').replace('A', '').replace('e', '').replace('E', '').replace('i', '')\
            .replace('I', '').replace('o', '').replace('O', '').replace('u', '').replace('U', '')
        await ctx.channel.send(dvl)

    @commands.command(aliases=['christmas', 'xmas'])
    async def isitchristmas(self, ctx):
        if date.today() == christmas:
            ctx.channel.send("Yes, it is Christmas today.")
        else:
            msg = f'No, it is not Christmas today. There are {(christmas - date.today()).days)} days until Christmas.'
            ctx.channel.send(msg)

    @commands.command(aliases=['halloween', 'hween', 'hwn'])
    async def isithalloween(self, ctx):
        if date.today() == halloween:
            ctx.channel.send("Yes, it is Halloween today.")
        else:
            msg = f'No, it is not Halloween today. There are {(halloween - date.today()).days)} days until Halloween.'
            ctx.channel.send(msg)

    @commands.command(description='This command might get you banned')
    async def ultimate_annoying_spam_command(self, ctx, *, member=None, times: int = None):
        """Want to annoy a member with mentions?"""
        channel = ctx.message.channel
        author = ctx.message.author
        message = ctx.message
        usage = f'```Usage: {ctx.prefix}ultimate_annoying_spam_command [@member] [times]```'

        if member or times is None:
            await ctx.channel.send(usage)
            return

        if times is None:
            times = 25

        if times > 100:
            times = 35

        if times is 0:
            sorry = f'Someone, not saying who, *cough cough {author}* felt sorry about using this command.'
            await ctx.channel.send(sorry)
            return

        if times < 0:
            chicken = "Well, that's just not enough times to annoy anybody. Don't chicken out now!"
            await ctx.channel.send(chicken)
            return

        await message.delete()

        for i in range(0, times):
            try:
                await channel.send(f'{member.mention} LOL')
            except Exception:
                pass

    @commands.command(aliases=['tinyurl'])
    async def tiny_url(self, ctx, str = None):

        apiurl = "http://tinyurl.com/api-create.php?url="
        tinyurl = urlopen(apiurl + str).read().decode("utf-8")
        usage = f'Usage: {ctx.prefix}tinyurl https://github.com/verixx/grokbot'
        url = ctx.message.starts_with('https://')
        if str is None:
            await ctx.channel.send(usage)
        if str is int:
            await ctx.channel.send(usage)
        if str is url:
            await ctx.channel.send(tinyurl)
        else:
            pass


def setup(bot):
    bot.add_cog(Misc(bot))
