from eris.events.types.eventbase import EventBase
from discord.message import Message


class MessageEvent(EventBase):

    def __init__(self, message: Message):
        self.type = 'message'
        self.actual = message
        self.body = message.content

    @classmethod
    def matches(cls, type: str, data: any):
        """ This class only handles messages from Discord. """
        return isinstance(data, Message)
