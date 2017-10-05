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
from discord.ext.commands import TextChannelConverter
from ext.paginator import PaginatorSession
#from ext import embedtobox
from PIL import Image
from contextlib import redirect_stdout
import traceback
import textwrap
import aiohttp
import inspect
import re
import io

dev_list = [
    180314310298304512,
    227620842903830528,
    168143064517443584,
    273381165229146112,
    319395783847837696,
    323578534763298816
]


class Developer:
    '''Useful commands to make your life easier'''

    def __init__(self, bot):
        self.bot = bot
        # self.lang_conv = load_json('data/langs.json')
        self._last_embed = None
        self._rtfm_cache = None
        self._last_google = None
        self._last_result = None

    @commands.command()
    async def paginate(self, ctx):
        session = PaginatorSession(ctx)
        for x in range(10):
            em = discord.Embed(title=f'Page: {x}', description='hello' * x)
            session.add_page(em)
        await session.run()

    @commands.command()
    async def cmd_help(self, ctx):
        """Test the help function"""
        await self.bot.send_cmd_help(ctx)

    @commands.command(aliases=["reload"])
    async def reloadcog(self, ctx, *, cog: str):
        """Reloads a cog"""
        if ctx.author.id in dev_list:
            cog = "cogs.{}".format(cog)
            await ctx.send("Attempting to reload {}...".format(cog))
            self.bot.unload_extension(cog)
            try:
                self.bot.load_extension(cog)
                await ctx.send("Successfully reloaded the {} cog!".format(cog))
            except Exception as e:
                await ctx.send(f"```py\nError loading cog: {cog}\n{e}\n```")

    @commands.command(pass_context=True, hidden=True, name='eval')
    async def _eval(self, ctx, *, body: str):
        """Evaluates a code"""
        if ctx.author.id in dev_list:
            env = {
                'bot': self.bot,
                'ctx': ctx,
                'channel': ctx.channel,
                'author': ctx.author,
                'guild': ctx.guild,
                'message': ctx.message,
                '_': self._last_result
            }

            env.update(globals())

            body = self.cleanup_code(body)

            stdout = io.StringIO()
            err = out = None

            to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

            try:
                exec(to_compile, env)
            except Exception as e:
                err = await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')
                return await err.add_reaction('\u2049')

            func = env['func']
            try:
                with redirect_stdout(stdout):
                    ret = await func()
            except Exception as e:
                value = stdout.getvalue()
                err = await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
            else:
                value = stdout.getvalue()
                if self.bot.token in value:
                    value = value.replace(self.bot.token, "[EXPUNGED]")
                if ret is None:
                    if value:
                        try:
                            out = await ctx.send(f'```py\n{value}\n```')
                        except:
                            out = await ctx.send('Result was too long to send.')
                else:
                    self._last_result = ret
                    try:
                        out = await ctx.send(f'```py\n{value}{ret}\n```')
                    except:
                        out = await ctx.send('Result was too long to send.')

            if out:
                to_log = self.cleanup_code(out.content)
                await out.add_reaction('\u2705')
            elif err:
                to_log = self.cleanup_code(err.content)
                await err.add_reaction('\u2049')
            else:
                to_log = 'No textual output.'
                await ctx.message.add_reaction('\u2705')

            if ctx.guild:
                serverid = ctx.guild.id
            else:
                serverid = None

            await self.log_eval(ctx, body, out, err, serverid)

    async def log_eval(self, ctx, body, out, err, serverid):
        if out:
            to_log = self.cleanup_code(out.content)
            color = discord.Color.green()
            name = 'Output'
        elif err:
            to_log = self.cleanup_code(err.content)
            color = discord.Color.red()
            name = 'Error'
        else:
            to_log = 'No textual output.'
            color = discord.Color.gold()
            name = 'Output'

        to_log = to_log.replace('`', '\u200b`')

        '''
        em = discord.Embed(color=color,timestamp=ctx.message.created_at)
        em.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
        em.add_field(name='Input', value=f'```py\n{body}\n```', inline=False)
        em.add_field(name=name, value=f'```{to_log}```')
        em.set_footer(text=f'User ID: {ctx.author.id} | Server ID: {serverid}')
        await self.bot.get_channel(364794381649051648).send(embed=em)
        '''
        e_input = discord.Embed(color=color, timestamp=ctx.message.created_at)
        e_input.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
        e_input.add_field(name='Input', value=f'```py\n{body}\n```', inline=False)
        e_input.set_footer(text=f'User ID: {ctx.author.id}')
        await self.bot.get_channel(364794381649051648).send(embed=e_input)
        e_output = discord.Embed(color=color, timestamp=ctx.message.created_at)
        e_output.set_author(name=f'{str(ctx.author)}: {name}', icon_url=ctx.author.avatar_url)
        e_output.description = f'```{to_log}```'
        await self.bot.get_channel(364794381649051648).send(embed=e_output)

    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

    @commands.command()
    async def set_val(self, ctx, field, *, value):
        self.bot.db.set_value(ctx.server.id, field, value)
        await ctx.send(f'Updated `{field}` to `{value}`')

    @commands.command()
    async def get_val(self, ctx, field):
        value = self.bot.db.get_value(ctx.guild.id, field)
        await ctx.send(f'Value for `{field}`: `{value}`')

    @commands.command(name='presence')
    async def _presence(self, ctx, status, *, message=None):
        """Change I'm Grok status!
        (Stream, Online, Idle, DND, Invisible, or clear it)
        """
        if ctx.author.id in dev_list:
            status = status.lower()
            emb = discord.Embed(title="Presence")
            emb.color = await ctx.get_dominant_color(ctx.author.avatar_url)
            file = io.BytesIO()
            if status == "online":
                await self.bot.change_presence(status=discord.Status.online, game=discord.Game(name=message))
                color = discord.Color(value=0x43b581).to_rgb()
            elif status == "idle":
                await self.bot.change_presence(status=discord.Status.idle, game=discord.Game(name=message))
                color = discord.Color(value=0xfaa61a).to_rgb()
            elif status == "dnd":
                await self.bot.change_presence(status=discord.Status.dnd, game=discord.Game(name=message))
                color = discord.Color(value=0xf04747).to_rgb()
            elif status == "invis" or status == "invisible":
                await self.bot.change_presence(status=discord.Status.invisible, game=discord.Game(name=message))
                color = discord.Color(value=0x747f8d).to_rgb()
            elif status == "stream":
                await self.bot.change_presence(status=discord.Status.online, game=discord.Game(name=message, type=1, url=f'https://www.twitch.tv/{message}'))
                color = discord.Color(value=0x593695).to_rgb()
            elif status == "clear":
                await self.bot.change_presence(game=None)
                emb.description = "Presence cleared."
                return await ctx.send(embed=emb)
            else:
                emb.description = "Please enter either `online`, `idle`, `dnd`, `invisible`, or `clear`."
                return await ctx.send(embed=emb)

            Image.new('RGB', (500, 500), color).save(file, format='PNG')
            emb.description = "Thank you for updating my Presence!"
            file.seek(0)
            emb.set_author(name=status.title(), icon_url="attachment://color.png")
            """
            try:
                await ctx.send(file=discord.File(file, 'color.png'), embed=emb)
            except discord.HTTPException:
                em_list = await embedtobox.etb(emb)
                for page in em_list:
                    await ctx.send(page)
            """

    @commands.command()
    async def source(self, ctx, *, command):
        '''See the source code for any command.'''
        if ctx.author.id in dev_list:
            source = str(inspect.getsource(self.bot.get_command(command).callback))
            fmt = '​`​`​`py\n' + source.replace('​`', '\u200b​`') + '\n​`​`​`'
            if len(fmt) > 2000:
                async with ctx.session.post("https://hastebin.com/documents", data=source) as resp:
                    data = await resp.json()
                key = data['key']
                return await ctx.send(f'Command source: <https://hastebin.com/{key}.py>')
            else:
                return await ctx.send(fmt)



def setup(bot):
    bot.add_cog(Developer(bot))
