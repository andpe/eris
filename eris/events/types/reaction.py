from eris.events.types.eventbase import EventBase
from collections import namedtuple
from discord.reaction import Reaction

ReactionTuple = namedtuple('ReactionTuple', ['action', 'reaction', 'user'])


class ReactionEvent(EventBase):

    def __init__(self, data: tuple):
        super().__init__(data)
        self.type = 'reaction'
        self.actual = ReactionTuple(action=data[0], reaction=data[1], user=data[2])
        self.body = None

    @classmethod
    def matches(cls, type, data):
        try:
            if len(data) > 0:
                return isinstance(data[1], Reaction)
        except:
            return False
