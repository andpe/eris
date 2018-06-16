from eris.events.types.eventbase import EventBase

import logging
import inspect

logging.basicConfig()
logger = logging.getLogger(__name__)


class AdminOnly(object):
    """ Decorator to restrict a command to a list of admins.

        Specify what offset the event parameter is on the command using the event_offset parameter or else this will not
        work.
    """

    offset = 1
    config = None

    @classmethod
    def register_config(cls, config):
        cls.config = config

    def __init__(self, event_offset=1):
        self.offset = event_offset

    def __call__(self, f):

        async def wrapped_f(*args, **kwargs):
            event: EventBase = args[self.offset]
            if str(event.actual.author.id) in self.__class__.config['admins']:
                res = await f(*args, **kwargs)
                return res
            else:
                return 0

        return wrapped_f