""" Precondition decorator.

Checks the precondition before allowing execution of the hook callback.
"""

from eris.events.hooks import HOOK_EAT_NONE


class HookPrecondition:

    """ Handle advanced preconditions to a hook. """

    def __init__(self, callback):
        self.callback = callback

    def __call__(self, func):
        async def wrapped_f(*args, **kwargs):
            if self.callback(*args, **kwargs):
                return await func(*args, **kwargs)

            return HOOK_EAT_NONE

        return wrapped_f
