""" Base module for bot modules. """
from __future__ import annotations

import inspect
import logging
from typing import TypeVar, Generic

from eris.core import Core
from eris.events.handler import EventHandler, PRIO_LOW

ClientType = TypeVar('ClientType', bound=Core)


class GenericModuleBase(Generic[ClientType]):

    """ Modules should always implement a few methods that lets us do what we need to register events. """

    eventhandler: EventHandler = None
    default_priority: int = PRIO_LOW
    client: ClientType = None
    LOGGER = None

    def __init__(self):
        self.LOGGER = logging.getLogger('.'.join([
            self.__class__.__module__, self.__class__.__qualname__
        ]))

    def scan_decorators(self):
        """ This method will scan the implementing class for decorated methods. """
        methods = inspect.getmembers(self, predicate=inspect.ismethod)
        for info in methods:
            if hasattr(info[1], 'hooks'):
                self.LOGGER.debug("Found hooks list on %s", info[1].__qualname__)
                for hook in info[1].hooks:
                    hook.callback = info[1]
                    self.register_hook(hook)

    def register(self):
        """ Register events with the eventhandler """
        raise NotImplementedError("This method has not been implemented on this module")

    def unregister(self):
        """ Deregister the events with the eventhandler. """
        self.eventhandler.unregister_module(str(self.__class__))

    def register_hook(self, hook):
        """ Register a hook with the eventhandler """
        self.LOGGER.debug('Registering hook (%r) for %s (prio: %s)', hook, str(self.__class__.__qualname__), self.default_priority)
        self.eventhandler.register_handler(str(self.__class__.__qualname__), self.default_priority, hook)


ModuleBase = GenericModuleBase[Core]
