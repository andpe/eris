from eris.events.hooks import HOOK_EAT_NONE


class HookPrecondition:

    """ Handle advanced preconditions to a hook. """

    def __init__(self, cb):
        self.cb = cb

    def __call__(self, f):
        async def wrapped_f(*args, **kwargs):
            if self.cb(*args, **kwargs):
                return await f(*args, **kwargs)
            else:
                return HOOK_EAT_NONE

        return wrapped_f