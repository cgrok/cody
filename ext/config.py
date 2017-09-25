import sqlite3
import json
import discord

class GuildConfig:

    '''Class to aid with server specific configuration.'''

    __slots__ = (
        'db', 'conn', 'cur', 'bot', 'id'
        )

    def __init__(self, database, id):
        self.db = database
        self.conn = database.conn
        self.cur = database.cur
        self.bot = database.bot
        self.id = id

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
        id = self.data.get('modlog')
        return self.bot.get_channel()

    @modlog.setter
    def modlog(self, channel):
        if isinstance(channel, int):
            pass
        elif isinstance(channel, discord.TextChannel):
            id = channel.id
            pass

    # TODO: Do the rest on the bottom

    @property
    def guild(self):
        return self.bot.get_guild(self.id)

    @property
    def name(self):
        return self.guild.name

    @property
    def welcome_channel(self):
        id = data.get('join_message_channel')
        return self.guild.get_channel(id)

    @property
    def leave_channel(self):
        id = data.get('leave_message_channel')
        return self.guild.get_channel(id)

    def add_prefix(self):
        pass # do stuff with db to add a prefix

    def remove_prefix(self):
        pass # do stuff with db to remove prefix




class ConfigDatabase:
    '''Database functions'''
    def __init__(self, bot):
        self.bot = bot
        self.path = "../data/config.db"
        self.conn = sqlite3.connect(self.path)
        self.cur = self.conn.cursor()
        self.create_config_table()

    def create_config_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS config 
            (server_id INTEGER PRIMARY KEY UNIQUE, 
            prefixes TEXT, 
            modlog_channel INTEGER,
            join_channel INTEGER, 
            leave_channel INTEGER,
            leave_enabled TEXT,
            autorole_enabled TEXT, 
            modlog_enabled TEXT,
            join_enabled TEXT, 
            join_message TEXT, 
            leave_message TEXT, 
            selfroles TEXT)""")

    def set_default_config(self, server_id):
        with self.conn:
            self.cur.execute("""
                INSERT INTO config VALUES(
                ?,?, # serverid and prefixes
                0, 0, 0, 0, 0, 0, 0, # Channel IDs and bools 
                "Welcome to {server.name}, {user.mention}!", # join message
                "Bye Bye {user.name}!", # leave message
                "[]" # selfroles
                )""",(server_id,"[\"g.\"]"))

    def get_server(self, server_id):
        """Returns a dict of all fields"""
        return GuildConfig(self, server_id)

    def get_data(self, server_id):
        self.cur.execute("SELECT * FROM config WHERE server_id = ?",(server_id,))
        columns = [x[0] for x in self.cur.description]
        rows = self.cur.fetchone()
        if rows is None:
            return None
        else:
            raw_dict = {k:v if '_enabled' not in k else bool(v) for k, v in zip(columns, rows)}
            raw_dict['prefixes'] = json.loads(raw_dict['prefixes'])
            raw_dict['selfroles'] = json.loads(raw_dict['selfroles'])
            return raw_dict

    def get_value(self, server_id, column):
        self.cur.execute("SELECT ? FROM config WHERE server_id = ?", (column, server_id))
        return self.cur.fetchone()

    def set_value(self, server_id, column, new_val):
        with self.conn:
            self.cur.execute("UPDATE config SET ? = ? WHERE server_id = ?", (column, new_val, server_id))





