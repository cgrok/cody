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
        await  ctx.channel.send(user.mention + ' has been unmuted.')





def setup(bot):
        bot.add_cog(Mod(bot))
