""" Eris example module that greets people. """
from eris.modules.base import ModuleBase
from eris.events.hooks import Hook, HOOK_EAT_NONE
from eris.events.types.eventbase import EventBase
from eris.decorators.ratelimited import RateLimit
from eris.decorators.precondition import HookPrecondition
from eris.decorators.admin import AdminOnly
import discord


# noinspection PyMethodMayBeStatic
class GreeterModule(ModuleBase):

    def register(self):
        hook = Hook('hi hook', 'message', self.handle_hi)
        self.register_hook(hook)

    def unregister(self):
        pass

    def handle_hi_precondition(self, event: EventBase):
        splits = event.actual.content.split(' ')
        if splits[0].lower() == 'hi' and len(splits) == 1:
            return True
        else:
            return False

    @AdminOnly()
    @HookPrecondition(handle_hi_precondition)
    @RateLimit(3, 1, cb=lambda x: x.actual.channel)
    async def handle_hi(self, event: EventBase) -> int:
        """ Handle messages containing "hi" """

        actual: discord.Message = event.actual
        name = actual.author.nick if hasattr(actual.author, 'nick') and actual.author.nick else actual.author.name
        await actual.channel.send("Hello %s!" % name)

        return HOOK_EAT_NONE
