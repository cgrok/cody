import sqlite3
import json
import discord

class GuildConfig:

    '''Class to aid with server specific configuration.

    Attributes
    ----------
    id: int
        The id of the server
    name: str
        The current name of the server
    leave_enabled: bool
        Dictates if the leave message is to be sent.
    autorole_enabled: bool
        Dictates if the autorole function is to be used
    log_enabled: bool
        Dictates if the modlog is active or not.
    prefixes: list
        Prefixes that the server has.
    '''

    __slots__ = (
        'autorole', 'autorole_enabled', 'leave_enabled', 
        'leave_message', 'modlog', 'log_enabled', 'name', 'prefixes', 
        'selfroles','id', 'join_enabled', 'join_message','db', 'bot'
        )

    def __init__(self, database, **data):
        self.db = database
        self.bot = db.bot
        self.data = data
        self.id = data.get('server_id')
        
    def from_data(self, data):
        self._join_enabled = data.get('join_enabled')
        self._leave_enabled = data.get('leave_enabled')
        self._autorole_enabled = data.get('autorole_enabled')
        self._log_enabled = data.get('log_enabled')
        self.prefixes = json.loads(data.get('prefixes', "['g.']"))
        self.selfroles = data.get('selfroles')

    @property
    def join_message(self):
        return self.data.get('join_message')
        # this needs to be chnaged to be dynamic
        # something like: self.db.get_join_message()

    @join_message.setter
    def join_message(self, msg):
        pass # do stuff to update the join message

    @property
    def leave_message(self):
        return data.get('leave_message')

    @leave_message.setter
    def leave_message(self, msg):
        pass # do stuff to update leave message

    @property
    def autorole(self):
        id = self.data.get('autorole')
        return discord.utils.get(self.guild.roles, id=id)

    @autorole.setter
    def autorole(self, role):
        if isinstance(role, int):
            pass # do stuff
        else:
            role = role.id
            pass # do stuff

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

    # TODO: restructure the db


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





class DataBase:
    '''Database functions'''
    def __init__(self, bot):
        self.bot = bot
        self.path = "../data/config.db"
        self.conn = sqlite3.connect(self.path)
        self.cur = self.conn.cursor()
        self.create_db()


    def create_db(self):
        with self.conn:
            struc = """(server_id INTEGER PRIMARY KEY UNIQUE, 
                        prefixes TEXT, 
                        modlog INTEGER, 
                        leave_enabled TEXT,
                        autorole_enabled TEXT, 
                        log_enabled TEXT,
                        join_enabled TEXT, 
                        join_message TEXT, 
                        leave_message TEXT, 
                        join_leave_channel INTEGER)"""

            cur = self.conn.execute(f"CREATE TABLE IF NOT EXISTS config {struc}")


    def get_server(self, id):
        """Returns a dict of all fields"""
        self.cur.execute(f"SELECT * FROM config WHERE server_id = {id}")
        columns = [x[0] for x in self.cur.description]
        rows = self.cur.fetchone()
        if rows is None:
            return None
        else:
            raw_dict = {k:v if '_enabled' not in k else bool(v) for k, v in zip(columns, rows)}
            return GuildConfig(self, **raw_dict)


