# Creating your own Cogs
This is a short guide on creating your own cogs for Grok Bot.
### Library    
All cogs have to be written in [discord.py 1.0.0.a](https://discordpy.readthedocs.io/en/rewrite/)   
### Data Storage
If you want to store any data in your cogs, it is highly encouraged you use [sqlite3](https://docs.python.org/2/library/sqlite3.html).  
### Example of a basic cog
```python
class Cog:
  def __init__(self, bot):
    self.bot = bot
    self.db = bot.db
    
  def _init_table_tags(
            self, tag, user_id: int, 
            value, *, table
            ):
    self.tags = table

def setup(bot):
    bot.add_cog(Cog(bot))
```

!> We are not obliged to provide support for creating cogs. For discord.py help, you can join their [official server](https://discord.gg/discord-api).

# Installing Cogs

### Important
You are only allowed to install cogs if you [self host this bot](https://verixx.github.io/grokbot/#/installation?id=self-hosting) and not use our instance of the bot. 

### How do I install a cog?


#### Key  
`{p}` - To be repalced with your prefix    
`[ ]` - Optional Parameters     
`< >` - Mandatory Parameters    

**Do not include these in your command**

1. Ensure you are the owner of the current instance.
2. Do `{p}install external <github link>`    
3. Do `{p}load <cog name>`
4. Test out the newly installed cog!
