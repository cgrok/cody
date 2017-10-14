import discord
from discord.ext import commands
from __main__ import dev_list


class CogManage:
    '''
    Description
    -----------
    Cog to aid with installing new cogs from online 
    and managing cogs. Everything here is owner only.

    Requirements
    ------------
    asyncio
    aiohttp
    '''

    BASE = 'https://raw.githubusercontent.com/{}/{}/master/{}'


    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db

    def __local_check(self, ctx):
        return ctx.author.id in dev_list

    @commands.command()
    async def uninstall(self, ctx, cogname):
        pass

    @commands.group(invoke_without_command=True)
    async def install(self, ctx, *, cogname):
        '''Download cogs from online.'''
        filename = f'cogs/{cogname}.py'
        url = self.BASE.format('grok-bot','cogs', filename)
        async with ctx.session.get(url) as resp:
            raw = await resp.text()
        await self.install_cog(ctx, raw, cogname)

    @install.command()
    async def custom(self, ctx, *, link):
        cogname = link.split('/')[-1]split('.')[0]
        async with ctx.session.get(link) as resp:
            raw = await resp.text()
        await self.install_cog(ctx, raw, cogname)

    async def install_cog(self, ctx, raw, cogname):
        if raw.strip() == '404: Not Found':
            return await ctx.send('Invalid cogname passed. Not Found.')
        else:
            with open(f'cogs/{cogname}.py', 'w') as f:
                f.write(raw)
        try:
            cog = self.bot.load_extension(f'cogs.{cogname}')
        except Exception as e:
            await ctx.send(f'Error on install: `{e}`')
        else:
            await self.send_info(ctx, cog)

    async def send_info(self, ctx, cog):

        all_commands = ''

        commands = self.bot.all_commands.items()
        pred = lambda c: c[1].instance is cog
        this_cog = list(filter(pred, commands))
        max_width = max([len(x[0]) for x in this_cog])

        for (name, cmd) in this_cog:
            entry = f'`{ctx.prefix}{name:<{max_width}} {cmd.short_doc}`\n'
            all_commands += entry

        em = discord.Embed(color=discord.Color.green())
        em.title = f'Cog: {type(cog).__name__}'
        em.description = 'Successfully Installed!'
        em.add_field(name='All Commands:', value=all_commands)

        await ctx.send(embed=em)


    ###############################################################
    # EVERYTHING BELOW THIS IS FUCKING SHIT CODE. REDO THIS PLEASE.
    ###############################################################

    # @commands.command(aliases=["reload"])
    # async def reloadcog(self, ctx, *, cog: str):
    #     '''Reloads a cog'''
    #     if ctx.author.id in dev_list:
    #         cog = f"cogs.{cog}"
    #         await ctx.send(f"Attempting to reload {cog}...")
    #         self.bot.unload_extension(cog)
    #         try:
    #             self.bot.load_extension(cog)
    #             await ctx.send(f"Successfully reloaded the {cog} cog!")
    #         except Exception as e:
    #             await ctx.send(f"​`​`​`py\nError loading cog: {cog}\n{e}\n​`​`​`")

    # @commands.command(aliases=["loadcog"])
    # async def load(self, ctx, *, cog: str):
    #     '''Load a cog'''
    #     if ctx.author.id in dev_list:
    #         cog = f"cogs.{cog}"
    #         await ctx.send(f"Attempting to load {cog}...")
    #         try:
    #             self.bot.load_extension(cog)
    #             await ctx.send(f"Successfully loaded the {cog} cog!")
    #         except Exception as e:
    #             await ctx.send(f"​`​`​`py\nError loading cog: {cog}\n{e}\n​`​`​`")

    # @commands.command(aliases=["unloadcog"])
    # async def unload(self, ctx, *, cog: str):
    #     '''Unload a cog'''
    #     if ctx.author.id in dev_list:
    #         cog = f"cogs.{cog}"
    #         await ctx.send(f"Unloading {cog}")
    #         self.bot.unload_extension(cog)

    ###############################################################
    # END OF SHIT CODE 
    ###############################################################


    # Remember to return bot.add_cog(cog) - I changed some stuff  

def setup(bot):
    cog = CogManage(bot)
    return bot.add_cog(cog)
