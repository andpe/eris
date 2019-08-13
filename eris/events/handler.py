from collections import OrderedDict

from eris.events.types.eventbase import EventBase
from eris.events.hooks import *
from eris.events.consts import PRIO_LOW, PRIO_MEDIUM, PRIO_HIGH


class EventHandler(object):

    """ Core event handler for the discord bot. """

    hooks = None
    template = None

    def __init__(self):
        # TODO: Decide if there's a better way to structure events (such as by type instead).
        self.hooks = OrderedDict()

    def register_module(self, module: str) -> bool:
        """ Register a module with the event handler. """
        if module in self.hooks:
            return False
        else:
            mod = OrderedDict()
            mod[PRIO_HIGH] = OrderedDict()
            mod[PRIO_MEDIUM] = OrderedDict()
            mod[PRIO_LOW] = OrderedDict()
            self.hooks[module] = mod

    def unregister_module(self, module: str):
        """ Unregister a module from the EventHandler. """
        if module in self.hooks:
            del self.hooks[module]

    async def handle(self, event: EventBase):
        """ Handle the events by looking through hooks. """
        eat = 0
        for module in self.hooks:
            for prio in self.hooks[module]:
                for hook_name in self.hooks[module][prio]:
                    hook = self.hooks[module][prio][hook_name]
                    if hook.match(event):
                        res = await hook.call(event)
                        eat = res if res is not None else 0

                    if eat & HOOK_EAT_PRIO == HOOK_EAT_PRIO:
                        break
                if eat & HOOK_EAT_MODULE == HOOK_EAT_MODULE:
                    break
            if eat & HOOK_EAT_SYSTEM == HOOK_EAT_SYSTEM:
                break

        return True

    def register_handler(self, module: str, priority: int, hook: Hook):
        """ Registers a hook with the event handler.

        Passing the same hook twice will simply overwrite the old one

        """
        if module not in self.hooks:
            self.register_module(module)

        # TODO: Verify that the hook fulfills the expected contract.
        self.hooks[module][priority][hook.name] = hook
