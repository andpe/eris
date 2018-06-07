from eris.events.types import *
from eris.events.types.eventbase import EventBase
from discord import Message
import inspect

class EventFactory(object):

    """ Factory for creating events to pass to the event handler. """

    @staticmethod
    def create(type: str, data: any) -> EventBase:

        glob = globals().copy()
        del glob['EventBase']

        # Find subclasses of EventBase
        classes = []
        for name in glob:
            if inspect.isclass(glob[name]) and issubclass(glob[name], EventBase):
                classes.append(glob[name])

        # Figure out who can handle this.
        for cls in classes:
            if cls.matches(type, data):
                return cls.get(data)

        raise NotImplementedError("Could not find a fitting event type")
