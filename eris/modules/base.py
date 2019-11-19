""" Base module for bot modules. """

from discord.client import Client

from eris.events.handler import EventHandler, PRIO_LOW


class ModuleBase:

    """ Modules should always implement a few methods that lets us do what we need to register events. """

    eventhandler: EventHandler = None
    default_priority: int = PRIO_LOW
    client: Client = None

    def register(self):
        """ Register events with the eventhandler """
        raise NotImplementedError("This method has not been implemented on this module")

    def unregister(self):
        """ Deregister the events with the eventhandler. """
        self.eventhandler.unregister_module(str(self.__class__))

    def register_hook(self, hook):
        """ Register a hook with the eventhandler """
        self.eventhandler.register_handler(str(self.__class__), self.default_priority, hook)
