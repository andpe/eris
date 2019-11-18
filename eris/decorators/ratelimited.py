""" Ratelimiting decorator for hook callbacks. """
from time import time
import logging

from eris.events.hooks import HOOK_EAT_NONE

from eris.decorators import BaseDecorator

logging.basicConfig()
LOGGER = logging.getLogger(__name__)


class RateLimit(BaseDecorator):
    """ Rate limit commands per minute or per five-second burst. """

    max_minute: int = None
    max_fs: int = None
    callback: callable = None
    hits: dict = None
    ttl = 120

    def __init__(self, max_minute: int, max_fs: int, callback: callable = None, static_fqn=None):
        self.max_minute = max_minute
        self.max_fs = max_fs
        self.callback = callback
        self.static_fqn = static_fqn

        if self.__class__.hits is None:
            self.__class__.hits = {}

    @classmethod
    def get(cls, bucket):
        """ Get the current number of hits for this bucket. """
        if bucket in cls.hits:
            return {
                'minute': len(list(filter(lambda x: time() - x <= 60, cls.hits[bucket]))),
                'fs': len(list(filter(lambda x: time() - x <= 5, cls.hits[bucket])))
            }

        return {
            'minute': 0,
            'fs': 0
        }

    @classmethod
    def incr(cls, bucket):
        """ Increase the hit counter for this bucket. """
        if bucket in cls.hits:
            cls.hits[bucket] = list(filter(lambda x: time() - x < cls.ttl, cls.hits[bucket]))
        else:
            cls.hits[bucket] = []

        cls.hits[bucket].append(time())
        return cls.get(bucket)

    def __call__(self, func):
        """ Handle the function call and wrap. """
        async def wrapped_f(*args, **kwargs):
            if self.callback is not None:
                key = self.callback(args[self._EVENT_OFFSET])
            else:
                key = None

            fqn = '.'.join([
                func.__module__, func.__qualname__
            ]) if self.static_fqn is None else self.static_fqn

            hitcount = self.__class__.get(fqn + ':' + str(key))

            # Make sure we're under the rate limit before calling.
            if hitcount['minute'] < self.max_minute and hitcount['fs'] < self.max_fs:
                res = await func(*args, **kwargs)
                if res is not None:
                    self.__class__.incr(fqn + ':' + key)
                    return res

            LOGGER.warning("function %s hit rate limit", fqn)
            return HOOK_EAT_NONE

        return wrapped_f
