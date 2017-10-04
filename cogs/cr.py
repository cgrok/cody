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
import json
import asyncio

class ClashRoyale:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def clan(self, ctx, tag=None, tag_type="clan"):
        '''Returns the stats of a clan.'''
        if tag == None:
            stats = self.bot.db.get_value(ctx.guild.id, "stats")
            stats = stats.split(" ")
            try:
                player_index = stats.index(str(ctx.author.id))
            except ValueError:
                return await ctx.send(f"Please save your Profile ID by doing `{ctx.prefix}save`.")
            tag = stats[player_index+1]
            tag_type = "player"
        tag = tag.replace("#", "")
        if tag_type == "player":
            url = f"http://api.cr-api.com/profile/{tag}"
            async with ctx.session.get(url) as d:
                data = await d.json()
            if data.get("error"):
                em = discord.Embed(color=discord.Color(value=0x33ff30), title="Clan", description="Invalid Player ID.")
                return await ctx.send(embed=em)
            if data['clan'] == None:
                em = discord.Embed(color=discord.Color(value=0x33ff30), title="Clan", description="Player is not in a clan.")
                return await ctx.send(embed=em)
            tag = data['clan']['tag']
            url = f"http://api.cr-api.com/clan/{tag}"
            async with ctx.session.get(url) as d:
                data = await d.json()
        elif tag_type == "clan":
            url = f"http://api.cr-api.com/clan/{tag}"
            async with ctx.session.get(url) as d:
                data = await d.json()      
            if data.get("error"):
                em = discord.Embed(color=discord.Color(value=0x33ff30), title="Clan", description="Invalid Clan ID.")
                return await ctx.send(embed=em) 
        else:
            em = discord.Embed(color=discord.Color(value=0x33ff30), title="Clan", description="Please only enter `player` for the tag type if necessary.")
            return await ctx.send(embed=em)

        em = discord.Embed(color=discord.Color(value=0x33ff30), title=f"{data['name']} (#{tag})", description=f"{data['description']}")
        em.set_author(name="Clan", url=f"http://cr-api.com/clan/{tag}", icon_url=f"http://api.cr-api.com{data['badge']['url']}")
        em.set_thumbnail(url=f"http://api.cr-api.com{data['badge']['url']}")
        em.add_field(name="Trophies", value=str(data['score']), inline=True)
        em.add_field(name="Type", value=data['typeName'], inline=True)
        em.add_field(name="Member Count", value=f"{data['memberCount']}/50", inline=True)
        em.add_field(name="Requirement", value=str(data['requiredScore']), inline=True)
        em.add_field(name="Donations", value=str(data['donations']), inline=True)
        em.add_field(name="Region", value=data['region']['name'])
        players = []
        for i in range(len(data['members'])):
            if i <= 2:
                players.append(f"{data['members'][i]['name']}: {data['members'][i]['trophies']}\n(#{data['members'][i]['tag']})")
        em.add_field(name="Top 3 Players", value="\n\n".join(players), inline=True)
        contributors = sorted(data['members'], key=lambda x: x['clanChestCrowns'])
        contributors = list(reversed(contributors))
        players = []
        for i in range(len(data['members'])):
            if i <= 2:
                players.append(f"{contributors[i]['name']}: {contributors[i]['clanChestCrowns']}\n(#{contributors[i]['tag']})")
        em.add_field(name="Top CC Contributors", value='\n\n'.join(players), inline=True)
        em.set_footer(text="Cog made by kwugfighter | Powered by cr-api", icon_url="http://cr-api.com/static/img/branding/cr-api-logo.png")
        await ctx.send(embed=em)


    @commands.command(aliases=['stats', 'p', 's'])
    async def profile(self, ctx, tag=None):
        '''Returns the stats of a player.'''
        if tag == None:
            stats = self.bot.db.get_value(ctx.guild.id, "stats")
            stats = stats.split(" ")
            try:
                player_index = stats.index(str(ctx.author.id))
            except ValueError:
                return await ctx.send(f"Please save your Profile ID by doing `{ctx.prefix}save`.")
            tag = stats[player_index+1]
        tag = tag.replace("#", "")
        url = f"http://api.cr-api.com/profile/{tag}"
        async with ctx.session.get(url) as d:
            data = await d.json()
        if data.get("error"):
            em = discord.Embed(color=discord.Color(value=0x33ff30), title="Profile", description="That's an invalid Player ID.")
            return await ctx.send(embed=em)
        em = discord.Embed(color=discord.Color(value=0x33ff30), title=data['name'], description=f"#{data['tag']}")
        try:
            em.set_author(name="Profile", url=f"http://cr-api.com/profile/{tag}", icon_url=f"http://api.cr-api.com{data['clan']['badge']['url']}")
        except:
            em.set_author(name="Profile", url=f"http://cr-api.com/profile/{tag}", icon_url=f"https://raw.githubusercontent.com/kwugfighter/cr-selfstats/master/data/clanless.png")
        em.set_thumbnail(url=f"http://api.cr-api.com{data['arena']['imageURL']}")
        if data['experience']['xpRequiredForLevelUp'] == "Max":
            to_level_up = "(Max Level)"
        else:
            to_level_up = f"({data['experience']['xp']}/{data['experience']['xpRequiredForLevelUp']})"
        em.add_field(name="Trophies", value=str(data['trophies']), inline=True)
        em.add_field(name="Personal Best", value=str(data['stats']['maxTrophies']), inline=True)
        em.add_field(name="Level", value=f"{data['experience']['level']} {to_level_up}", inline=True)
        if data['globalRank'] == None:
            global_ranking = "N/A"
        else:
            global_ranking = data['globalRank']
        em.add_field(name="Global Rank", value=global_ranking)
        em.add_field(name="Total Donations", value=str(data['stats']['totalDonations']), inline=True)
        em.add_field(name="Win Rate (Excluding Draws)", value=f"{data['games']['wins']/(data['games']['wins']+data['games']['losses'])*100}%", inline=True)
        em.add_field(name="Legendary Trophies", value=str(data['stats']['legendaryTrophies']), inline=True)
        em.add_field(name="Win Streak", value=str(data['games']['currentWinStreak']), inline=True)
        em.add_field(name="Arena", value=data['arena']['name'], inline=True)
        em.add_field(name="Favorite Card", value=data['stats']['favoriteCard'].replace('_', ' ').title(), inline=True)
        em.add_field(name="Wins", value=str(data['games']['wins']), inline=True)
        em.add_field(name="Losses", value=str(data['games']['losses']), inline=True)
        em.add_field(name="Draws", value=str(data['games']['draws']), inline=True)
        try:
            em.add_field(name="Clan Info", value=f"{data['clan']['name']}\n(#{data['clan']['tag']})\n{data['clan']['role']}", inline=True)
        except:
            em.add_field(name="Clan Info", value=f"N/A", inline=True)

        try:
            if data['previousSeasons'][0]['seasonEndGlobalRank'] == None:
                ranking = "N/A"
            else:
                ranking = data['previousSeasons'][0]['seasonEndGlobalRank'] + "trophies"
            em.add_field(name="Season Results", value=f"Season Finish: {data['previousSeasons'][0]['seasonEnding']}\nSeason Highest: {data['previousSeasons'][0]['seasonHighest']}\nGlobal Rank: {ranking}", inline=True)
        except:
            em.add_field(name="Season Results", value=f"Season Finish: N/A\nSeason Highest: N/A\nGlobal Rank: N/A", inline=True)
        try:
            supermag = data['chestCycle']['superMagicalPos']-data['chestCycle']['position']
        except:
            supermag = "N/A"
        try:
            leggie = data['chestCycle']['legendaryPos']-data['chestCycle']['position']
        except:
            leggie = "N/A"
        try:
            epic = data['chestCycle']['epicPos']-data['chestCycle']['position']
        except:
            epic = "N/A"
        em.add_field(name="Upcoming Chests", value=f"Super Magical: {supermag}\nLegendary: {leggie}\nEpic: {epic}", inline=True)
        deck = f"{data['currentDeck'][0]['name'].replace('_', ' ').title()}: Lvl {data['currentDeck'][0]['level']}"
        for i in range(1,len(data['currentDeck'])):
            deck += f"\n{data['currentDeck'][i]['name'].replace('_', ' ').title()}: Lvl {data['currentDeck'][i]['level']}"
        em.add_field(name="Battle Deck", value=deck, inline=True)
        offers = ""
        if data['shopOffers']['legendary'] > 0:
            offers += f"Legendary Chest: {data['shopOffers']['legendary']} days\n"
        if data['shopOffers']['epic'] > 0:
            offers += f"Epic Chest: {data['shopOffers']['epic']} days\n"
        if data['shopOffers']['arena'] != None:
            offers += f"Arena Pack: {data['shopOffers']['arena']} days"
        if offers == "":
            offers = "None"
        em.add_field(name="Shop Offers", value=offers, inline=True)

        em.set_footer(text="Cog made by kwugfighter | Powered by cr-api", icon_url="http://cr-api.com/static/img/branding/cr-api-logo.png")
        await ctx.send(embed=em)

    @commands.command()
    async def members(self, ctx, tag=None, tag_type="clan"):
        '''Returns the members of a clan.'''
        if tag == None:
            stats = self.bot.db.get_value(ctx.guild.id, "stats")
            stats = stats.split(" ")
            try:
                player_index = stats.index(str(ctx.author.id))
            except ValueError:
                return await ctx.send(f"Please save your Profile ID by doing `{ctx.prefix}save`.")
            tag = stats[player_index+1]
            tag_type = "player"
        tag = tag.replace("#", "")
        if tag_type == "player":
            url = f"http://api.cr-api.com/profile/{tag}"
            async with ctx.session.get(url) as d:
                data = await d.json()
            if data.get("error"):
                em = discord.Embed(color=discord.Color(value=0x33ff30), title="Clan", description="Invalid Player ID.")
                return await ctx.send(embed=em)
            if data['clan'] == None:
                em = discord.Embed(color=discord.Color(value=0x33ff30), title="Clan", description="Player is not in a clan.")
                return await ctx.send(embed=em)
            tag = data['clan']['tag']
            url = f"http://api.cr-api.com/clan/{tag}"
            async with ctx.session.get(url) as d:
                data = await d.json()
        elif tag_type == "clan":
            url = f"http://api.cr-api.com/clan/{tag}"
            async with ctx.session.get(url) as d:
                data = await d.json()      
            if data.get("error"):
                em = discord.Embed(color=discord.Color(value=0x33ff30), title="Clan", description="Invalid Clan ID.")
                return await ctx.send(embed=em) 
        else:
            em = discord.Embed(color=discord.Color(value=0x33ff30), title="Clan", description="Please only enter `player` for the tag type if necessary.")
            return await ctx.send(embed=em)
        em = discord.Embed(color=discord.Color(value=0x33ff30), title=f"{data['name']} (#{tag})", description='Page 1')
        em.set_author(name="Clan", url=f"http://cr-api.com/clan/{tag}", icon_url=f"http://api.cr-api.com{data['badge']['url']}")
        em.set_thumbnail(url=f"http://api.cr-api.com{data['badge']['url']}")
        for player in data['members']:
            if player['currentRank'] == 26:
                em.set_footer(text="Cog made by kwugfighter | Powered by cr-api", icon_url="http://cr-api.com/static/img/branding/cr-api-logo.png")
                await ctx.send(page)
                em = discord.Embed(color=discord.Color(value=0x33ff30), title=f"{data['name']} (#{tag})", description='Page 2')
                em.set_thumbnail(url=f"http://api.cr-api.com{data['badge']['url']}")
            em.add_field(name=player['name'], value=f"(#{player['tag']})\nTrophies: {player['score']}\nDonations: {player['donations']}\nCrowns: {player['clanChestCrowns']}\nRole: {player['roleName']}")
        em.set_footer(text="Cog made by kwugfighter | Powered by cr-api", icon_url="http://cr-api.com/static/img/branding/cr-api-logo.png")
        await ctx.send(embed=em)

    @commands.command()
    async def save(self, ctx, tag):
        stats = self.bot.get_value(ctx.guild.id, "stats")
        self.bot.db.set_value(ctx.guild.id, "stats", f"{stats} {ctx.author.id} {tag}")
        await ctx.send("Profile saved.")

def setup(bot):
    bot.add_cog(ClashRoyale(bot))