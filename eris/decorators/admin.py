""" AdminOnly decorator.

Limits the use of a command to a predefined list of admins.
"""
import logging
from functools import wraps

from eris.config import Config
from eris.decorators import BaseDecorator
from eris.events.hooks import HOOK_EAT_NONE
from eris.events.types.eventbase import EventBase

logging.basicConfig()
LOGGER = logging.getLogger(__name__)


class AdminOnly(BaseDecorator):

    """ Decorator to restrict a command to a list of admins.

        Specify what offset the event parameter is on the command using the event_offset parameter or else this will not
        work.
    """

    config: Config = None

    @classmethod
    def register_config(cls, config):
        """ Register the config with the class. """
        cls.config = config

    def __init__(self):
        pass

    def __call__(self, func):
        """ Handle the function call. """
        cls = self.__class__

        @wraps(func)
        async def wrapped_f(*args, **kwargs):
            event: EventBase = args[self._EVENT_OFFSET]

            # Ignore E1135 and 36 because of a false positive here.
            # pylint: disable=E1135
            if not cls.config.admins:
                return HOOK_EAT_NONE

            # pylint: disable=E1136
            if str(event.actual.author.id) in cls.config.admins:
                res = await func(*args, **kwargs)
                return res

            return HOOK_EAT_NONE

        return wrapped_f
