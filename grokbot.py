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
from ext.context import CustomContext
from ext.config import ConfigDatabase
from collections import defaultdict
import asyncio
import aiohttp
import datetime
import psutil
import time
import json
import sys
import os
import re
import sqlite3
import traceback
import textwrap

class StatsBoard:
    def __init__(self, bot, channel, base=None):
        self.bot = bot
        self.channel = channel
        self.base = base
        self.running = bool(base)

    @property
    def current_stats(self):
        em = discord.Embed()
        status = None
        me = self.channel.guild.me
        status = str(me.status)
        if status == 'online':
            em.set_author(name="I'm Grok - Live Stats", icon_url='https://i.imgur.com/wlh1Uwb.png')
            em.color = discord.Color.green()
        elif status == 'dnd':
            status = 'maintenance'
            em.set_author(name="I'm Grok - Live Stats", icon_url='https://i.imgur.com/lbMqojO.png')
            em.color = discord.Color.purple()
        else:
            em.set_author(name="I'm Grok - Live Stats", icon_url='https://i.imgur.com/dCLTaI3.png')
            em.color = discord.Color.red()

        total_online = len({m.id for m in self.bot.get_all_members() if m.status is not discord.Status.offline})
        total_unique = len(self.bot.users)
        channels = sum(1 for g in self.bot.guilds for _ in g.channels)

        now = datetime.datetime.utcnow()
        delta = now - self.bot.uptime
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        fmt = '{h}h {m}m {s}s'
        if days:
            fmt = '{d}d ' + fmt
        uptime = fmt.format(d=days, h=hours, m=minutes, s=seconds)
        g_authors = 'verixx, fourjr, kwugfighter, FloatCobra, XAOS1502'
        
        em.add_field(name='Current Status', value=str(status).title())
        em.add_field(name='Uptime', value=uptime)
        em.add_field(name='Latency', value=f'{self.bot.ws.latency*1000:.2f} ms')
        em.add_field(name='Guilds', value=len(self.bot.guilds))
        em.add_field(name='Members', value=f'{total_online}/{total_unique} online')
        em.add_field(name='Channels', value=f'{channels} total')
        memory_usage = self.bot.process.memory_full_info().uss / 1024**2
        cpu_usage = self.bot.process.cpu_percent() / psutil.cpu_count()
        em.add_field(name='RAM Usage', value=f'{memory_usage:.2f} MiB')
        em.add_field(name='CPU Usage',value=f'{cpu_usage:.2f}% CPU')
        em.add_field(name='Commands Run', value=sum(self.bot.commands_used.values()))
        em.add_field(name='Messages', value=self.bot.messages_sent)
        # em.add_field(name='Authors', value=g_authors, inline=False)
        em.set_footer(text=f'Powered by discord.py {discord.__version__}')

        return em

    async def make_base(self):
        self.base = await self.channel.send(embed=self.current_stats)
        self.running = True
        with open('data/config.json') as f:
            data = json.load(f)
        with open('data/config.json', 'w') as f:
            data['base'] = self.base.id
            json.dump(data, f)

    async def force_update(self):
        await self.base.edit(embed=self.current_stats)

    async def run(self):
        if not self.running:
            await self.make_base()

        if isinstance(self.base, int):
            try:
                self.base = await self.channel.get_message(self.base)
            except:
                await self.make_base()

        while self.running:
            try:
                await self.base.edit(embed=self.current_stats)
            except discord.HTTPException:
                await self.make_base()
            await asyncio.sleep(5)



class GrokBot(commands.Bot):
    '''
    GrokBot!
    '''
    _mentions_transforms = {
        '@everyone': '@\u200beveryone',
        '@here': '@\u200bhere'
    }

    _mention_pattern = re.compile('|'.join(_mentions_transforms.keys()))

    def __init__(self, **attrs):
        super().__init__(command_prefix=self.get_pre)
        self.uptime = datetime.datetime.utcnow()
        self.db = ConfigDatabase(self)
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.process = psutil.Process()
        self._extensions = [x.replace('.py', '') for x in os.listdir('cogs') if x.endswith('.py')]
        self.messages_sent = 0
        self.commands_used = defaultdict(int)
        self.loop.create_task(self.statsboard())
        #self.remove_command('help')
        self.add_command(self.ping)
        self.add_command(self.shutdown)
        self.add_command(self.maintenance)
        self.load_extensions()
        self.load_community_extensions()

    def load_extensions(self, cogs=None, path='cogs.'):
        '''Loads the default set of extensions or a seperate one if given'''
        for extension in cogs or self._extensions:
            try:
                self.load_extension(f'{path}{extension}')
                print(f'Loaded extension: {extension}')
            except Exception as e:
                traceback.print_exc()

    def load_community_extensions(self):
        '''Loads up community extensions.'''
        with open('data/community_cogs.txt') as fp:
            to_load = fp.read().splitlines()
        if to_load:
            self.load_extensions(to_load, 'cogs.community.')

    @property
    def token(self):
        '''Returns your token wherever it is'''
        with open('./data/config.json') as f:
            config = json.load(f)
            if config.get('TOKEN') == "your_token_here":
                if not os.environ.get('TOKEN'):
                    self.run_wizard()
            else:
                token = config.get('TOKEN').strip('\"')

        return os.environ.get('TOKEN') or token

    @staticmethod
    async def get_pre(bot, message):
        '''Returns the prefix.'''
        with open('./data/config.json') as f: # TODO: server specific prefixes
            prefix = json.load(f).get('PREFIX')
        return os.environ.get('PREFIX') or prefix or 'g.'

    @staticmethod
    def run_wizard():
        '''Wizard for first start'''
        print('------------------------------------------')
        token = input('Enter your token:\n> ')
        print('------------------------------------------')
        prefix = input('Enter a prefix for your bot:\n> ')
        data = {
                "TOKEN" : token,
                "PREFIX" : prefix,
            }
        with open('./data/config.json','w') as f:
            f.write(json.dumps(data, indent=4))
        print('------------------------------------------')
        print('Restarting...')
        print('------------------------------------------')
        os.execv(sys.executable, ['python'] + sys.argv)

    @classmethod
    def init(bot, token=None):
        '''Starts the actual bot'''
        bot = bot()
        safe_token = token or bot.token.strip('\"')
        try:
            bot.run(safe_token, reconnect=True)
        except Exception as e:
            print(e)

    async def on_connect(self):
        print('---------------\n'
              'GrokBot connected!')

    async def on_ready(self):
        '''Bot startup, sets uptime.'''
            

        for guild in self.guilds: # sets default configs for all guilds.
            if self.db.get_data(guild.id) is None:
                self.db.set_default_config(guild.id)

        print(textwrap.dedent(f'''
        ---------------
        Client is ready!
        ---------------
        Authors: verixx, fourjr, kwugfighter, 
                 FloatCobra, XAOS1502, Protty, 
                 Dark knight, darthgimdalf
        ---------------
        Logged in as: {self.user}
        User ID: {self.user.id}
        ---------------
        '''))

    async def on_command(self, ctx):
        cmd = ctx.command.qualified_name.replace(' ', '_')
        self.commands_used[cmd] += 1

    async def process_commands(self, message):
        '''Utilises the CustomContext subclass of discord.Context'''
        ctx = await self.get_context(message, cls=CustomContext)
        if ctx.command is None:
            return
        await self.invoke(ctx)

    async def on_message(self, message):
        '''Extra calculations'''
        if message.author == self.user:
            return
        self.messages_sent += 1
        self.last_message = time.time()
        await self.process_commands(message)

    async def statsboard(self):
        await self.wait_until_ready()
        channel = self.get_channel(364720838743949313)
        with open('data/config.json') as f:
            base = json.load(f).get('base')
        self.statsboard = StatsBoard(self, channel, base)
        await self.statsboard.run()

    @commands.command()
    async def ping(self, ctx):
        """Pong! Returns your websocket latency."""
        em = discord.Embed()
        em.title ='Pong! Websocket Latency:'
        em.description = f'{self.ws.latency * 1000:.4f} ms'
        em.color = 0x00FFFF
        try:
            await ctx.send(embed=em)
        except discord.HTTPException:
            em_list = await embedtobox.etb(emb)
            for page in em_list:
                await ctx.send(page)

    @commands.command()
    async def maintenance(self, ctx):
        if str(ctx.guild.me.status) == 'dnd':
            await ctx.send('Going back to normal.')
            await self.change_presence(status=discord.Status.online, game=None)
            return await self.statsboard.force_update()
        await self.change_presence(status=discord.Status.dnd, game=discord.Game(name='under maintenance.'))
        await ctx.send('Going into maintenance mode.')
        await self.statsboard.force_update()

    @commands.command()
    async def shutdown(self, ctx, maintenance=None):
        if maintenance:
            await self.change_presence(status=discord.Status.dnd)
        else:
            await self.change_presence(status=discord.Status.offline)
        await self.statsboard.force_update()
        await ctx.send('Shutting Down...')
        self.session.close()
        await self.logout()


if __name__ == '__main__':
    GrokBot.init('MzYxNDgyNjcxNDUwMzU3NzYy.DLWaCQ.xsaaBNrG0-g4O54DukLv3hAnwwE')
