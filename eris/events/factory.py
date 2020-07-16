""" Event factory for Eris. """
import inspect
from importlib import import_module

from eris.events.types.eventbase import EventBase


class EventFactory:

    """ Factory for creating events to pass to the event handler. """

    classes = []

    @staticmethod
    def init():
        """ Initialize the list of classes that handle events for us. """
        events = import_module('eris.events.types', '*')

        # Find subclasses of EventBase
        for name in events.__all__:
            if getattr(events, name) is not EventBase \
                    and inspect.isclass(getattr(events, name)) \
                    and issubclass(getattr(events, name), EventBase):
                EventFactory.classes.append(getattr(events, name))

    @staticmethod
    def create(event_type: str, data: any) -> EventBase:
        """ Return an event instance that handles the incoming event type. """
        # Figure out who can handle this.
        for cls in EventFactory.classes:
            if cls.matches(event_type, data):
                return cls.get(data)

        raise NotImplementedError("Could not find a fitting event type")
