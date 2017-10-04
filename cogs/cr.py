'''
MIT License

Copyright (c) 2017 kwugfighter

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
import aiohttp
import string
from cogs import embeds
import json


class TagCheck(commands.Converter):
    '''
    Main converter: 
    Takes in input and converts it into a user id if its a mention.
    Otherwise checks if its a valid tag.
    '''
    def __init__(self):
        self.check = 'PYLQGRJCUV0289'

    async def convert(self, ctx, arg):
        if arg == 'desc':
            return 'desc'
        if len(ctx.message.mentions):
            return ID(arg.strip(string.punctuation))
        u_check = lambda x: arg in [str(x), str(x.id), x.name]
        user = discord.utils.find(u_check, ctx.guild.members)
        if user:
            return ID(str(user.id))
        tag = arg.strip('#').upper()
        if any(i not in self.check for i in tag):
            await ctx.send('Hashtags should only contain these characters:\n'
                           '**Numbers:** 0, 2, 8, 9\n'
                           '**Letters:** P, Y, L, Q, G, R, J, C, U, V')

            raise commands.BadArgument('Incorrect Tag')
        return HashTag(tag)

class HashTag:
    '''Distinguishes HashTags from ID'''
    def __init__(self, tag):
        self.tag = tag
class ID:
    '''Distinguishes ID from HashTags'''
    def __init__(self, _id):
        self.id = str(_id)

class Stats:
    '''Main StatsBot commands.'''
    def __init__(self, bot):
        self.bot = bot
        self.token = open('data/token').read()
        self.headers = {'Authorization': self.token}
        self.base = 'http://harmiox.com:3001/cr/v1'

    async def get_player(self, tag):
        '''Request player data.'''
        async with self.bot.session.get(self.base + '/players/' + tag, headers=self.headers) as resp:
            return await resp.json()

    async def get_clan(self, tag):
        '''Request clan data.'''
        async with self.bot.session.get(self.base + '/clans/' + tag, headers=self.headers) as resp:
            return await resp.json()

    @commands.command()
    async def clan(self, ctx, discrim : TagCheck = None):
        '''Clan information.'''
        await self.parse_command(ctx, discrim, embeds.parse_clan, clan=True)

    @commands.command()
    async def profile(self, ctx, *, discrim: TagCheck=None):
        '''Player profile data.'''
        await self.parse_command(ctx, discrim, embeds.parse_profile)

    @commands.command() 
    async def stats(self, ctx, *, discrim : TagCheck=None):
        '''Basic player stats.'''
        await self.parse_command(ctx, discrim, embeds.parse_stats)

    @commands.command()
    async def chests(self, ctx, *, discrim : TagCheck=None):
        '''Player chest cycle.'''
        await self.parse_command(ctx, discrim, embeds.parse_chests_command)

    @commands.command()
    async def offers(self, ctx, *, discrim : TagCheck=None):
        '''Player shop offers.'''
        await self.parse_command(ctx, discrim, embeds.parse_offers_command)

    @commands.group(invoke_without_command=True)
    async def deck(self, ctx, *, discrim : TagCheck=None):
        '''Player deck.'''
        await self.parse_command(ctx, discrim, embeds.parse_deck_command, deck=True)

    @deck.command()
    async def desc(self, ctx, *, description):
        '''Deck description.'''
        with open('data/saved.json') as f:
            data = json.load(f)
            data.get(str(ctx.author.id))['deck'] = description
        with open('data/saved.json','w') as f:
            f.write(json.dumps(data, indent=4))
        await ctx.send('Successfully set deck description to `{}`'.format(description))

    @commands.command()
    async def save(self, ctx, discrim : TagCheck):
        '''Save's a player tag to discord profile.'''
        player_data = await self.get_player(discrim.tag)
        clan_tag = player_data['clan'].get('tag')
        with open('data/saved.json') as f:
            data = json.load(f)
            data[str(ctx.author.id)] = {'tag': discrim.tag, 'clan': clan_tag}
        with open('data/saved.json','w') as f:
            f.write(json.dumps(data, indent=4))
        await ctx.send('Successfuly saved your tag!')

    def resave_clan_tag(self, id, tag):
        '''Resave clan tag in background.'''
        with open('data/saved.json') as f:
            data = json.load(f)
            data[id]['clan'] = tag
        with open('data/saved.json', 'w') as f:
            f.write(json.dumps(data, indent=4))

    async def parse_command(self, ctx, discrim, parser, deck=None, clan=None):
        '''Generate embeds.'''
        if not discrim:
            discrim = ID(ctx.author.id)
        if discrim == 'desc':
            return
        if isinstance(discrim, HashTag):
            if clan:
                data = await self.get_clan(discrim.tag)
                embed = parser(data)
                return await ctx.send(embed=embed)
            data = await self.get_player(discrim.tag)
            embed = parser(data)
            await ctx.send(embed=embed)
        else:
            with open('data/saved.json') as f:
                data = json.load(f)
            tags = data.get(discrim.id)
            if tags:
                if clan:
                    if not tags.get('clan'):
                        if discrim.id == str(ctx.author.id):
                    	    return await ctx.send('You don\'t have a clan.')
                        else:
                            return await ctx.send('That person does not have a clan!')
                    data = await self.get_clan(tags.get('clan'))
                    embed = parser(data)
                    return await ctx.send(embed=embed)
                data = await self.get_player(tags.get('tag'))
                embed = parser(data)
                if deck:
                    if tags.get('deck'):
                        embed.description = '*{}*'.format(tags.get('deck'))
                    else:
                        embed.description = '*Did you know you could set your own deck description using ' \
                                            '`{}deck desc <description>`?*'.format(ctx.prefix)
                self.resave_clan_tag(discrim.id, data['clan'].get('tag'))
                await ctx.send(embed=embed)
            else:
                if discrim.id == str(ctx.author.id):
                    await ctx.send('You dont have a saved tag. do `{}save #YourTag`'.format(ctx.prefix))
                else:
                    await ctx.send('That person does not have a saved tag.')


def setup(bot):
    bot.add_cog(Stats(bot))
