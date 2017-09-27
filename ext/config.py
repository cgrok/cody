import sqlite3
import json
import shlex
import discord

class GuildConfig:

    '''Class to aid with guild specific configuration.'''

    __slots__ = (
        'db', 'conn', 'cur', 'bot', 'id'
        )

    def __init__(self, database, id):
        self.db = database
        self.conn = database.conn
        self.cur = database.cur
        self.bot = database.bot
        self.id = id


    def __str__(self):
        return json.dumps(self.db.get_data(self.id), indent=4)
        
    @property
    def join_message(self):
        return self.db.get_value(self.id, 'join_message')

    @join_message.setter
    def join_message(self, msg):
        return self.db.set_value(self.id, 'join_message', msg)

    @property
    def leave_message(self):
        return self.db.get_value(self.id, 'leave_message')

    @leave_message.setter
    def leave_message(self, msg):
        return self.db.set_value(self.id, 'leave_message', msg)

    @property
    def autorole(self):
        id = self.db.get_value(self.id, 'autorole')
        return discord.utils.get(self.guild.roles, id=id)

    @autorole.setter
    def autorole(self, role):
        if isinstance(role, int):
            id = role
        else:
            id = role.id
        return self.db.set_value(self.id, 'autorole', id)

    @property
    def modlog(self):
        id = self.db.get_value(self.id,'modlog')
        return self.bot.get_channel()

    @modlog.setter
    def modlog(self, channel):
        if isinstance(channel, int):
            id = channel
        elif isinstance(channel, discord.TextChannel):
            id = channel.id
        return self.db.set_value(self.id, 'modlog_channel', id)

    @property
    def guild(self):
        return self.bot.get_guild(self.id)

    @property
    def welcome_channel(self):
        id = data.get('join_message_channel')
        return self.guild.get_channel(id)

    @welcome_channel.setter
    def set_welcome_channel(self, channel):
        if isinstance(channel, int):
            id = channel
        elif isinstance(channel, discord.TextChannel):
            id = channel.id
        return self.db.set_value(self.id, 'welcome_channel', id)

    @property
    def leave_channel(self):
        id = data.get('leave_message_channel')
        return self.guild.get_channel(id)

    @leave_channel.setter
    def set_leave_channel(self, channel):
        if isinstance(channel, int):
            id = channel
        elif isinstance(channel, discord.TextChannel):
            id = channel.id
        return self.db.set_value(self.id, 'leave_channel', id)

    @property
    def prefixes(self):
        return json.loads(self.db.get_value(self.id, 'prefixes'))
        

    @prefixes.setter
    def set_prefixes(self, prefixes):
        '''
        String input:
            Prefixes must be seperated with a single space
            Prefixes must be wrapped in double quotes if they are multi word
        '''
        if isinstance(prefixes, list):
            set_val = json.dumps(prefixes)
        if isinstance(prefixes, str):
            set_val = json.dumps(shlex.split(prefixes))
        return self.db.set_value(self.id, 'prefixes', set_val)

    @property
    def leave_enabled(self):
        return bool(self.db.get_value(self.id, 'leave_enabled'))

    @leave_enabled.setter
    def toggle_leave(self):
        value = int(not self.db.get_value(self.id, 'leave_enabled'))
        return self.db.set_value(self.id, 'leave_enabled', value)
    
    @property
    def join_enabled(self):
        return bool(self.db.get_value(self.id, 'join_enabled'))
    
    @join_enabled.setter
    def toggle_join(self):
        value = int(not self.db.get_value(self.id, 'join_enabled'))
        return self.db.set_value(self.id, 'join_enabled', value)
    
    @property
    def autorole_enabled(self):
        return bool(self.db.get_value(self.id, 'autorole_enabled'))
    
    @autorole_enabled.setter
    def toggle_autorole(self):
        value = int(not self.db.get_value(self.id, 'autorole_enabled'))
        return self.db.set_value(self.id, 'autorole_enabled', value)
    
    @property
    def modlog_enabled(self):
        return bool(self.db.get_value(self.id, 'modlog_enabled'))
        
    @modlog_enabled.setter
    def toggle_modlog(self):
        value = int(not self.db.get_value(self.id, 'modlog_enabled'))
        return self.db.set_value(self.id, 'modlog_enabled', value)

    @property
    def selfroles(self):
        return json.loads(self.db.get_value(self.id, "selfroles"))
    
    @selfroles.setter
    def set_selfroles(self, roles):
        # Prefixes must be seperated with a single space
        # Prefixes must be wrapped in double quotes if they are multi word
        return self.db.set_value(self.id, 'selfroles', json.dumps(shlex.split(roles)))

class ConfigDatabase:
    '''Database functions'''
    slots = ('bot','path','conn','cur')

    def __init__(self, bot):
        self.bot = bot
        self.path = "data/config.db"
        self.conn = sqlite3.connect(self.path)
        self.cur = self.conn.cursor()
        self.create_config_table()

    def create_config_table(self):
        with self.conn:
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS config
                (guild_id INTEGER PRIMARY KEY UNIQUE,
                prefixes TEXT,
                modlog_channel INT,
                join_channel INT,
                leave_channel INT,
                leave_enabled INT(1),
                autorole_enabled INT(1),
                modlog_enabled INT(1),
                join_enabled INT(1),
                join_message TEXT,
                leave_message TEXT,
                selfroles TEXT,
                autorole INT)""")

    def set_default_config(self, guild_id):
        with self.conn:
            default = (
                guild_id,"[\"g.\"]",0,0,0,0,0,0,0,
                "Welcome {user.mention} to {guild.name}","Bye Bye {user.name}!","[]",0
                )
            self.cur.execute(f"INSERT INTO config VALUES {default}")

    def get_guild(self, guild_id):
        """Returns a dict of all fields"""
        return GuildConfig(self, guild_id)

    def get_data(self, guild_id):
        """Returns a raw dict of all fields"""
        self.cur.execute("SELECT * FROM config WHERE guild_id = ?",(guild_id,))
        columns = [x[0] for x in self.cur.description]
        rows = self.cur.fetchone()
        if rows is None:
            return None
        else:
            raw_dict = {k:v if '_enabled' not in k else bool(v) for k, v in zip(columns, rows)}
            raw_dict['prefixes'] = json.loads(raw_dict['prefixes'])
            raw_dict['selfroles'] = json.loads(raw_dict['selfroles'])
            return raw_dict

    def get_value(self, guild_id, column):
        self.cur.execute(f"SELECT {column} FROM config WHERE guild_id = {guild_id}")
        return self.cur.fetchone()

    def set_value(self, guild_id, column, new_val):
        with self.conn:
            self.cur.execute(f"UPDATE config SET {column} = ? WHERE guild_id = {guild_id}", (new_val,))
