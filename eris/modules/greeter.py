from eris.modules.base import ModuleBase
from eris.events.hooks import Hook, HOOK_EAT_NONE
from eris.events.types.eventbase import EventBase
from eris.decorators.ratelimited import RateLimit
import discord


class GreeterModule(ModuleBase):

    def register(self):
        hook = Hook('hi hook', 'message', self.handle_hi)
        self.register_hook(hook)

    def unregister(self):
        pass

    @RateLimit(2, 1, 'event', cb=lambda x: x.actual.channel)
    async def handle_hi(self, event: EventBase) -> int:
        """ Handle messages containing "hi" """
        actual: discord.Message = event.actual

        splits = actual.content.split(' ')

        if splits[0].lower() == 'hi' and len(splits) == 1:
            await self.client.send_message(actual.channel, "Hello %s!" % actual.author.name)

        return HOOK_EAT_NONE
