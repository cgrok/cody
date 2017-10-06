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
from discord.ext import commands

class Mod:

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, user: discord.Member):
        await ctx.channel.send(f"RIP {user.name}.")
        await user.kick()


    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def ban(self, ctx, user: discord.Member):
        await ctx.channel.send(f"Goodbye {user.name}.")
        await user.ban()


    @commands.command()
    @commands.has_permissions(manage_roles = True)
    async def addrole(self, ctx, user: discord.Member, role: str):
        roler = discord.utils.get(ctx.guild.roles, name=role)

        if roler is not None:
            try:
                await user.add_roles(roler)
            except discord.Forbidden:
                await ctx.channel.send("You don't have permission to do this.")
        else:
            await ctx.channel.send("I can't add a nonexistent role.")

    @commands.command()
    @commands.has_permissions(manage_roles = True)
    async def removerole(self, ctx, user: discord.Member, role: str):
        roler = discord.utils.find(ctx.guild.roles, name=role)

        if roler is not None:
            try:
                await user.add_roles(roler)
            except discord.Forbidden:
                await ctx.channel.send("You don't have permission to do this.")
        else:
            await ctx.channel.send("I can't remove a nonexistent role.")

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def mute(self, ctx, user: discord.Member):

        await ctx.channel.set_permissions(user, send_messages=False)
        await ctx.channel.send(user.mention + " has been muted.")



    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def unmute(self,ctx, user: discord.Member):

        await ctx.channel.set_permissions(user, send_messages=True)
        await ctx.channel.send(user.mention + ' has been unmuted.')

    @commands.command(aliases=['del', 'p', 'prune'], bulk=True)
    async def purge(self, ctx, limit: int):
        """Clean a number of messages"""
        await ctx.message.delete()
        deleted = await ctx.channel.purge(limit=limit + 1)
        await ctx.channel.send(f'Successfully deleted {len(deleted)} message(s)', delete_after=6)

    @commands.command()
    async def clean(self, ctx, limit: int = 15):
        """Clean a number of bot's messages"""
        await ctx.message.delete()
        deleted = await ctx.channel.purge(limit=limit + 1, check=lambda m: m.author == self.bot.user)
        await ctx.channel.send(f'Successfully deleted {len(deleted)} message(s)', delete_after=5)


def setup(bot):
        bot.add_cog(Mod(bot))
