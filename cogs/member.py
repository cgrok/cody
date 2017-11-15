import discord
from discord.ext import commands
import asyncio
import shlex
import json
from ext import config

class Member:
    """Manage Member events."""

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.db


    def _role_from_string(self, server, rolename, roles=None):
        if roles is None:
            roles = server.roles

        roles = [r for r in roles if r is not None]
        role = discord.utils.find(lambda r: r.name.lower() == rolename.lower(), roles)
        return role

    @commands.group(no_pm=True)
    async def memberset(self, ctx):

        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)
            em = discord.Embed(color=discord.Colour.red(), description="Member Settings")
            try:
                em.add_field(name="Join Message Enabled", value=ctx.config.join_enabled, inline=False)
                em.add_field(name="Leave Message Enabled", value=ctx.config.leave_enabled, inline=False)
                em.add_field(name="Welcome Channel", value=ctx.config.welcome_channel, inline=False)
                em.add_field(name="Leave Channel", value=ctx.config.leave_channel, inline=False)
                em.add_field(name="Join Message", value=ctx.config.join_message, inline=False)
                em.add_field(name="Leave Message", value=ctx.config.leave_message, inline=False)
                try:
                    em.add_field(name="Selfroles", value=", ".join(ctx.config.selfroles))
                except:
                    em.add_field(name="Selfroles", value="No selfroles set")
            except Exception as e:
                print(e)
            await ctx.send(embed=em)


    @memberset.command(aliases=["welcome"], no_pm=True)
    async def join(self, ctx, enabled:str, channel:discord.TextChannel=None, *, message=None):
        """Join message settings
        Arguments for message:
        `{name}` outputs the Member's username.
        `{guild}` outputs the Guild name.
        `{mention}` mentions the user"""
        enable = ["enabled","on","true","yes"]
        if enabled.lower() in enable:
            ctx.config.join_enabled = True
            await ctx.send("Turned join message on.")
        else:
            ctx.config.join_enabled = False
            await ctx.send("Turned join message off.")
        if channel is not None:
            ctx.config.welcome_channel = channel.id
            await channel.send(f"{ctx.author.mention} :information_source:, I will now send join messages here")
        ctx.config.join_message = str(message)
        await ctx.send(":information_source: Welcome message set!")

    @memberset.command(aliases=["goodbye"], no_pm=True)
    async def leave(self, ctx, *, channel:discord.TextChannel=None, enabled:str, message:str=None):
        """Leave message settings
        Arguments for message:
        `{name}` outputs the Member's username.
        `{guild}` outputs the Guild name."""
        enable = ["enabled","on","true","yes"]
        if enabled.lower() in enable:
            ctx.config.leave_enabled = True
            await ctx.send("Turned leave message on.")
        else:
            ctx.config.leave_enabled = False
            await ctx.send("Turned leave message off.")
        if channel is not None:
            ctx.config.leave_channel = channel.id
            await channel.send(f"{ctx.author.mention} :information_source:, I will now send leave messages here")
        ctx.config.leave_message = message
        await ctx.send(":information_source: Leave message set!")

    @memberset.command(no_pm=True)
    async def selfroles(self, ctx, *, rolelist=None):
        """Set which roles users can set themselves.
        Seperate roles with a space, if rolename contains a space, wrap in double quotes,
        Example:
        Human "Non Human" Robot"""
        if rolelist is None:
            await ctx.send("Selfrole list cleared.")
            ctx.config.selfroles = []
            return
        unparsed_roles = list(map(lambda r: r.strip(), shlex.split(rolelist)))
        parsed_roles = list(map(lambda r: self._role_from_string(ctx.guild, r), unparsed_roles))
        if len(unparsed_roles) != len(parsed_roles):
            not_found = set(unparsed_roles) - {r.name for r in parsed_roles}
            await ctx.send(f"These roles were not found: {not_found}\n\nPlease try again.")
        parsed_role_set = list({r.id for r in parsed_roles})

        ctx.config.selfroles = parsed_role_set
        await ctx.send(ctx.config.selfroles)
        await ctx.send(f"Selfroles successfully set to: {parsed_role_set}")

    @commands.group(no_pm=True, invoke_without_command=True)
    async def selfrole(self, ctx, *, rolename):
        """Allows users to set their own roles.
        Configurable using `memberset`"""
        if len(ctx.config.selfroles) == 0:
            await ctx.send("No self assignable roles found for this server.")
            return
        role_names = [discord.utils.get(ctx.guild.roles, id=x.id).name for x in ctx.config.selfroles]
        f = self._role_from_string
        roles = [f(ctx.guild, r) for r in role_names if r is not None]
        role_to_add = self._role_from_string(ctx.guild, rolename, roles=roles)
        try:
            await ctx.author.add_roles(role_to_add)
        except discord.errors.Forbidden:
            await ctx.send("I don't have permission to do that.")
        except AttributeError:
            await ctx.send("That role isn't self assignable")
        else:
            await ctx.send("Role added.")

    async def on_member_join(self, member):
        if self.config.get_guild(member.guild.id).join_enabled:
            await self.config.get_guild(member.guild.id).welcome_channel.send(self.config.get_guild(member.guild.id).join_message.format(name=member, guild=member.guild, mention=member.mention, member=member))
        if self.config.get_guild(member.guild.id).autorole_enabled:
            await member.add_roles(self.config.get_guild(member.guild.id).autorole)

    async def on_member_remove(self, member):
        if self.config.get_guild(member.guild.id).leave_enabled:
            await self.config.get_guild(member.guild.id).send(self.config.get_guild(member.guild.id).leave_message.format(name=member.name, guild=member.guild))

def setup(bot):
        n = Member(bot)
        return bot.add_cog(n)
