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


    @commands.command(no_pm=True)
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, user: discord.Member):
        '''Kicks a user if you have appropriate permissions'''
        await ctx.channel.send(f"RIP {user.name}.")
        await user.kick()


    @commands.command(no_pm=True)
    @commands.has_permissions(kick_members = True)
    async def ban(self, ctx, user: discord.Member):
        '''Bans a user if you have appropriate permissions'''
        await ctx.channel.send(f"Goodbye {user.name}.")
        await user.ban()


    @commands.command(no_pm=True)
    @commands.has_permissions(manage_roles = True)
    async def addrole(self, ctx, user: discord.Member, role: str):
        '''Adds a role to a user if you have appropriate permissions'''
        roler = discord.utils.get(ctx.guild.roles, name=role)

        if roler is not None:
            try:
                await user.add_roles(roler)
            except discord.Forbidden:
                await ctx.channel.send("You don't have permission to do this.")
        else:
            await ctx.channel.send("I can't add a nonexistent role.")

    @commands.command(no_pm=True)
    @commands.has_permissions(manage_roles = True)
    async def removerole(self, ctx, user: discord.Member, role: str):
        '''Removes a role from a user if you have appropriate permissions'''
        roler = discord.utils.find(ctx.guild.roles, name=role)

        if roler is not None:
            try:
                await user.add_roles(roler)
            except discord.Forbidden:
                await ctx.channel.send("You don't have permission to do this.")
        else:
            await ctx.channel.send("I can't remove a nonexistent role.")

    @commands.command(no_pm=True)
    @commands.has_permissions(kick_members = True)
    async def mute(self, ctx, user: discord.Member):
        '''Mutes member using channel overrides. Requires Kick Members Permission'''
        await ctx.channel.set_permissions(user, send_messages=False)
        await ctx.channel.send(user.mention + " has been muted.")



    @commands.command(no_pm=True)
    @commands.has_permissions(kick_members = True)
    async def unmute(self,ctx, user: discord.Member):
        '''Unmute member using channel overrides. Requires Kick Members Permission'''
        await ctx.channel.set_permissions(user, send_messages=True)
        await ctx.channel.send(user.mention + ' has been unmuted.')

    @commands.command(aliases=['del', 'p', 'prune'], bulk=True)
    async def purge(self, ctx, limit: int):
        '''Clean a number of messages'''
        await ctx.message.delete()
        deleted = await ctx.channel.purge(limit=limit + 1)
        await ctx.channel.send(f'Successfully deleted {len(deleted)} message(s)', delete_after=6)

    @commands.command(no_pm=True)
    async def clean(self, ctx, limit: int = 15):
        '''Clean a number of bot's messages'''
        await ctx.message.delete()
        deleted = await ctx.channel.purge(limit=limit + 1, check=lambda m: m.author == self.bot.user)
        await ctx.channel.send(f'Successfully deleted {len(deleted)} message(s)', delete_after=5)

    @commands.group(no_pm=True)
    async def modset(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @modset.command(no_pm=True)
    @commands.has_permissions(manage_roles=True)
    async def autorole(self, ctx, *, enabled:str, role:discord.Role = None):
        '''Set autorole configurations.'''
        enable = ["enable","on","true","yes"]
        if enabled.lower() in enable:
            ctx.config.autorole_enabled = True
            await ctx.send("Turned autorole on.")
        else:
            ctx.config.autorole_enabled = False
            await ctx.send("Turned autorole off.")
        if role is not None:
            ctx.config.autorole = role.id
            await ctx.send(f"Set autorole to {discord.utils.get(ctx.guild.roles,id=role.id)}")

    @modset.command(no_pm=True)
    @commands.has_permissions(view_audit_log=True)
    async def modlog(self, ctx, *, enabled:str, channel:discord.TextChannel = None):
        '''Setup the Moderation Log for your guild'''
        enable = ["enabled","on","true","yes"]
        if enabled.lower() in enable:
            ctx.config.modlog_enabled = True
            await ctx.send("Turned modlog on.")
        else:
            ctx.config.modlog_enabled = False
            await ctx.send("Turned modlog off.")
        if channel is not None:
            ctx.config.modlog_channel = channel.id
            await ctx.send(f"Set modlog channel to {self.bot.get_channel(channel.id)}")

def setup(bot):
    return bot.add_cog(Mod(bot))
