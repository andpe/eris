""" Eris example module that greets people. """
import discord

from eris.decorators.admin import AdminOnly
from eris.decorators.precondition import HookPrecondition
from eris.decorators.ratelimited import RateLimit
from eris.events.hooks import Hook, HOOK_EAT_NONE
from eris.events.types.eventbase import EventBase
from eris.modules.base import ModuleBase


# noinspection PyMethodMayBeStatic
class GreeterModule(ModuleBase):

    """ Example module that greets certain users when they say 'hi' """

    def register(self):
        hook = Hook('hi hook', 'message', self.handle_hi)
        self.register_hook(hook)

    def unregister(self):
        pass

    # pylint: disable=R0201
    def handle_hi_precondition(self, event: EventBase):
        """ Handle people saying hi. """
        splits = event.actual.content.split(' ')
        if splits[0].lower() == 'hi' and len(splits) == 1:
            return True

        return False

    @AdminOnly()
    @HookPrecondition(handle_hi_precondition)
    @RateLimit(3, 1, callback=lambda x: x.actual.channel)
    async def handle_hi(self, event: EventBase) -> int:
        """ Handle messages containing "hi" """

        actual: discord.Message = event.actual
        name = actual.author.nick if hasattr(actual.author, 'nick') and actual.author.nick else actual.author.name
        await actual.channel.send("Hello %s!" % name)

        return HOOK_EAT_NONE
