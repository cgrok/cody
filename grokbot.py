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
import textwrap


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
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.process = psutil.Process()
        self.extensions = [x.replace('.py', '') for x in os.listdir('cogs') if x.endswith('.py')]
        self.messages_sent = 0
        self.commands_used = defaultdict(int)
        self.remove_command('help')
        self.add_command(self.ping)
        self.load_extensions()
        self.load_community_extensions()

    def load_extensions(self, cogs=None, path='cogs.'):
        '''Loads the default set of extensions or a seperate one if given'''
        for extension in cogs or self.extensions:
            try:
                self.load_extension(f'{path}{extension}')
                print(f'Loaded extension: {extension}')
            except Exception as e:
                print(f'LoadError: {extension}\n'
                      f'{type(e).__name__}: {e}')

    def load_community_extensions(self):
        '''Loads up community extensions.'''
        with open('./data/community_cogs.txt') as fp:
            to_load = fp.read().splitlines()
        self.load_extensions(to_load, 'cogs.community')

    @property
    def token(self):
        '''Returns your token wherever it is'''
        with open('./data/config.json') as f:
            config = json.load(f)
            if config.get('TOKEN') == "your_token_here":
                if not os.environ.get('TOKEN'):
                    self.run_wizard()
            else:
                #token = config.get('TOKEN').strip('\"')
                token = "MzYxNDgyNjcxNDUwMzU3NzYy.DKkwmw.MZF4orBpH2xBZi1isx0s5MvvppU"
        return os.environ.get('TOKEN') or token

    @staticmethod
    async def get_pre(bot, message):
        '''Returns the prefix.'''
        with open('./data/config.json') as f: # TODO: server specific prefixes
            prefix = json.load(f).get('PREFIX')
        return os.environ.get('PREFIX') or prefix or 'r.'

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
        if not hasattr(self, 'uptime'):
            self.uptime = datetime.datetime.utcnow()
        print(textwrap.dedent(f'''
        ---------------
        Client is ready!
        ---------------
        Authors: verixx, fourjr, kwugfighter, FloatCobra, add the rest here bois
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

    @commands.command()
    async def ping(self, ctx):
        """Pong! Returns your websocket latency."""
        em = discord.Embed()
        em.title ='Pong! Websocket Latency:'
        em.description = f'{self.ws.latency * 1000:.4f} ms'
        em.color = await ctx.get_dominant_color(ctx.author.avatar_url)
        try:
            await ctx.send(embed=em)
        except discord.HTTPException:
            em_list = await embedtobox.etb(emb)
            for page in em_list:
                await ctx.send(page)
    class db:
        '''Holds all the server info and bot info'''
        def __init__(self):
            self.path = "./data/config.db"
            self.conn = sqlite3.connect(self.path)
            self.cur = self.conn.cursor()
            with self.conn:
                struc = "(server_id INTEGER PRIMARY KEY UNIQUE, prefixes TEXT, modlog INTEGER, serverlog INTEGER,leave_enabled TEXT,autorole_enabled TEXT, log_enabled TEXT,join_enabled TEXT, join_message TEXT, leave_message TEXT, join_leave_channel INTEGER)"
                self.conn.execute(f"CREATE TABLE IF NOT EXISTS config {struc}")
                # I've stored all the bools as text because it's simple and it works
        #note to self: use json.dumps(list) to store list of prefixes in db
        #ps: use json.loads() to get the list back

        def get_server(self, id):
            """Returns a dict of all fields"""
            self.conn.execute(f"SELECT * FROM config WHERE server_id = {id}")
            row = self.cur.fetchone()
            if row is None:
                return None
            else:
                return {"server_id":row[0], "prefixes":row[1], "modlog":row[2], "serverlog":row[3], "leave_enabled":bool(row[4]), "autorole_enabled":bool(row[4]), "log_enabled":bool(row[5]), "join_enabled":bool(row[6]), "join_message":row[7], "leave_message":row[8], "join_leave_channel":row[9]}
if __name__ == '__main__':
    GrokBot.init()
