""" Reaction type event. """
from collections import namedtuple

from discord.reaction import Reaction

from eris.events.types.eventbase import EventBase

ReactionTuple = namedtuple('ReactionTuple', ['action', 'reaction', 'user'])


class ReactionEvent(EventBase):

    """ A wrapper class for reaction events on Discord. """

    def __init__(self, data: tuple):
        super().__init__(data)
        self.type = 'reaction'
        self.actual = ReactionTuple(action=data[0], reaction=data[1], user=data[2])
        self.body = None

    @classmethod
    def matches(cls, event_type, data):
        try:
            if data:
                return isinstance(data[1], Reaction)
        except IndexError:
            pass

        return False
