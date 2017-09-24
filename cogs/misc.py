
class Misc:
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def invite(self, ctx):
        """Official url to invite bot to your server."""
        inviter = discord.utils.oauth_url(self.bot.user.id, permissions=discord.Permissions(permissions=8))
        await ctx.channel.send(f'Invite me to *__your__* server with this link: \n\n<{inviter}>')

    @commands.command()
    async def esrever(self, ctx, *, msg:str = None):
        """debmE ni ,snosaer esuaceb sdrawkcab setirW"""
        e = discord.Embed()
        e.colour = discord.Colour(0x8e44ad)
        if msg == None:
            usage = 'Write a message after command'
            e.description = usage
        if msg != None:
            e.description = f'\N{LEFTWARDS BLACK ARROW} `{msg.lower()[::-1]}`'
        await ctx.channel.send(embed=e)
        await ctx.delete_message(msg)

def setup(bot):
    bot.add_cog(Misc(bot))
