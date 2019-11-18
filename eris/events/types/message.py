""" Message type event. """
from discord.message import Message

from eris.events.types.eventbase import EventBase


class MessageEvent(EventBase):

    """ Message-handling event class. """

    def __init__(self, message: Message):
        super().__init__(message)

        self.type = 'message'
        self.actual = message
        self.body = message.content

    @classmethod
    def matches(cls, event_type: str, data: any):
        """ This class only handles messages from Discord. """
        return event_type == 'message' and isinstance(data, Message)
