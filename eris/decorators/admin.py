from eris.events.types.eventbase import EventBase

import logging

logging.basicConfig()
logger = logging.getLogger(__name__)


class AdminOnly(object):

    kw_key = None
    config = None

    @classmethod
    def register_config(cls, config):
        cls.config = config

    def __init__(self, kw_key='event'):
        self.kw_key = kw_key

    def __call__(self, f):

        def wrapped_f(*args, **kwargs):
            event: EventBase = kwargs[self.kw_key]
            if str(event.actual.user.id) in self.__class__.config['admins']:
                return f(*args, **kwargs)
            else:
                return 0

        return wrapped_f