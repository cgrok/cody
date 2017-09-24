

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
        'announce_channel', 'autorole', 'autorole_enabled', 'leave_enabled', 
        'leave_message', 'log_channel', 'log_enabled', 'name', 'prefixes', 
        'selfroles','id', 'join_enabled', 'join_message','join_message_channel',
        'leave_message_channel'
        )

    def __init__(self, **data):
        self.id = data.get('id')
        self.join_enabled = False
        self.leave_enabled = False
        self.autorole_enabled = False
        self.log_enabled = False
        self.from_data(data)

    def from_data(self, data):
        self.name = data.get('name')
        self.prefixes = data.get('prefixes', ['g.'])
        self.join_message = data.get('join_message')
        self.join_message_channel = data.get('join_message_channel')
        self.leave_message = data.get('join_message')
        self.leave_message_channel = data.get('leave_message_channel')
        self.autorole = data.get('autorole')
        self.selfroles = data.get('selfroles')
        self.announce_channel = data.get('announce_channel')
        self.log_channel = data.get('log_channel')

    def add_prefix(self, prefix):
        self.prefixes += [prefix]

    def remove_prefix(self, prefix):
        try:
            self.prefixes.remove(prefix)
        except:
            return False