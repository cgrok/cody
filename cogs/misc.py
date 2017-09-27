from datetime import date
import discord
from discord.ext import commands

halloween = date(2017, 10, 31)
christmas = date(2017, 12, 25)

class Misc:
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def invite(self, ctx):
        """Official url to invite bot to your server."""
        inviter = discord.utils.oauth_url(self.bot.user.id, permissions=discord.Permissions(permissions=8))
        await ctx.channel.send(f'Invite me to *__your__* server with this link: \n\n<{inviter}>')

    @commands.command()
    async def reverse(self, ctx, *, msg:str = None):
        """Writes backwards because reasons, in Embed"""
        e = discord.Embed()
        e.colour = discord.Colour(0x8e44ad)
        if msg == None:
            usage = 'Write a message after command'
            e.description = usage
        else:
            e.description = f'\N{LEFTWARDS BLACK ARROW} `{msg.lower()[::-1]}`'
        await ctx.channel.send(embed=e)
        await ctx.delete_message(msg)
        
    @commands.command(aliases=['dvwl'])
    async def devowel(self, ctx, *text):
        devoweled = text.replace('a','').replace('A','').replace('e','').replace('E','').replace('i','').replace('I','').replace('o','').replace('O','').replace('u','').replace('U','')
        await ctx.channel.send(devoweled)

    @commands.command(aliases=['christmas','xmas'])
    async def isitchristmas(self, ctx):
        if date.today() == christmas:
            ctx.channel.send("Yes, it is Christmas today.")
        else:
            ctx.channel.send("No, it is not Christmas today. There are {} days until Christmas.".format((christmas - date.today()).days))

    @commands.command(aliases=['halloween','hween','hwn'])
    async def isithalloween(self, ctx):
        if date.today() == halloween:
            ctx.channel.send("Yes, it is Halloween today.")
        else:
            ctx.channel.send("No, it is not Halloween today. There are {} days until Halloween.".format((halloween - date.today()).days))

def setup(bot):
    bot.add_cog(Misc(bot))
