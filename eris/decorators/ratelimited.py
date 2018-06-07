from time import time
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)


class RateLimit(object):

    max_minute: int = None
    max_fs: int = None
    kw_key: str = None
    cb: callable = None
    hits: dict = None

    def __init__(self, max_minute: int, max_fs: int, kw_key: str=None, cb: callable=None, static_key=None):
        self.max_minute = max_minute
        self.max_fs = max_fs
        self.kw_key = kw_key
        self.cb = cb if cb is not None else lambda kw: kw
        self.static_key = static_key

        if self.__class__.hits is None:
            self.__class__.hits = {}

    @classmethod
    def get(cls, bucket):
        if bucket in cls.hits:
            return {
                'minute': len(list(filter(lambda x: time() - x <= 60, cls.hits[bucket]))),
                'fs': len(list(filter(lambda x: time() - x <= 5, cls.hits[bucket])))
            }
        else:
            return {
                'minute': 0,
                'fs': 0
            }

    @classmethod
    def incr(cls, bucket):

        if bucket in cls.hits:
            cls.hits[bucket] = list(filter(lambda x: time() - x < 120, cls.hits[bucket]))
        else:
            cls.hits[bucket] = []

        cls.hits[bucket].append(time())
        return cls.get(bucket)

    def __call__(self, f):
        # Make sure we haven't exceeded the

        async def wrapped_f(*args, **kwargs):
            if isinstance(self.kw_key, str):
                key = self.kw_key
            else:
                key = self.cb(kwargs[self.kw_key])

            fqn = '.'.join([
                f.__module__, f.__qualname__
            ]) if self.static_key is None else self.static_key

            hitcount = self.__class__.get(fqn + ':' + key)

            # Make sure we're under the rate limit before calling.
            if hitcount['minute'] < self.max_minute and hitcount['fs'] < self.max_fs:
                res = await f(*args, **kwargs)
                if res is not None:
                    self.__class__.incr(f.__name__ + ':' + key)
            else:
                # HOOK_EAT_NONE
                logger.warning("function %s hit rate limit", f.__name__)
                return 0

        return wrapped_f