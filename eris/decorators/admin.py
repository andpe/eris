from eris.events.types.eventbase import EventBase
from eris.decorators import BaseDecorator

import logging

logging.basicConfig()
LOGGER = logging.getLogger(__name__)


class AdminOnly(BaseDecorator):
    """ Decorator to restrict a command to a list of admins.

        Specify what offset the event parameter is on the command using the event_offset parameter or else this will not
        work.
    """

    config = None

    @classmethod
    def register_config(cls, config):
        cls.config = config

    def __init__(self):
        pass

    def __call__(self, f):

        async def wrapped_f(*args, **kwargs):
            event: EventBase = args[self._EVENT_OFFSET]

            if str(event.actual.author.id) in self.__class__.config['admins']:
                res = await f(*args, **kwargs)
                return res
            else:
                return 0

        return wrapped_f
