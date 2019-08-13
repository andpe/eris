from eris.decorators.admin import AdminOnly
from eris.modules.base import ModuleBase
from eris.events.types.eventbase import EventBase
from discord.user import User


class AdminModule(ModuleBase):

    blocked_users = []

    def is_blocked(self, user: User):
        pass

    @AdminOnly()
    def handle_block(self, event: EventBase):
        pass

    @AdminOnly()
    def handle_unblock(self, event: EventBase):
        pass

    def register(self):
        pass

    def unregister(self):
        pass
