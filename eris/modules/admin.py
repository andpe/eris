""" Admin module.

Example module for handling admin users and commands.
"""
from discord.user import User

from eris.decorators.admin import AdminOnly
from eris.events.types.eventbase import EventBase
from eris.modules.base import ModuleBase


class AdminModule(ModuleBase):

    """ Example module for handling admin users and commands. """

    blocked_users = []

    def is_blocked(self, user: User):
        """ Check if a user is blocked. """
        pass

    @AdminOnly()
    def handle_block(self, event: EventBase):
        """ Handle block commands. """
        pass

    @AdminOnly()
    def handle_unblock(self, event: EventBase):
        """ Handle unblock commands. """
        pass

    def register(self):
        """ Register our hooks. """
        pass

    def unregister(self):
        """ Unregister our hooks. """
        pass
