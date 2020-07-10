""" Precondition decorator.

Checks the precondition before allowing execution of the hook callback.
"""
from functools import wraps

from eris.decorators import BaseDecorator
from eris.events.hooks import HOOK_EAT_NONE


class HookPrecondition(BaseDecorator):
    """ Handle advanced preconditions to a hook. """

    def __init__(self, callback):
        self.callback = callback

    def __call__(self, func):
        @wraps(func)
        async def wrapped_f(*args, **kwargs):
            if self.callback(*args, **kwargs):
                return await func(*args, **kwargs)

            return HOOK_EAT_NONE

        return wrapped_f
