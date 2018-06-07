""" Main module for the discord bot. """
import discord
import logging

from eris.events.factory import EventFactory
from eris.events.handler import EventHandler
from eris.config import Config
from eris.modules.base import ModuleBase
from eris.decorators.admin import AdminOnly

from importlib import import_module

logging.basicConfig()
logger = logging.getLogger(__name__)


class Core(discord.Client):

    """ Main class for handling the bot logic. """

    eventhandler = None
    config = None
    modules = None

    def __init__(self, config, *args, **kwargs):
        """ Create a new bot with the specified config. """
        self.eventhandler = EventHandler()
        self.modules = {}

        # Load the configuration and validate it.
        with open(config, 'r') as f:
            import json
            cfg = json.load(f)
        self.config = Config(cfg)

        AdminOnly.register_config(self.config)

        # Carry on as normal.
        super().__init__(*args, **kwargs)

    async def on_message(self, message):
        """ Handles incoming messages. """

        if self.eventhandler:
            event = EventFactory.create('message', message)
            await self.eventhandler.handle(event)
        else:
            logger.warning("No eventhandler registered... somehow, carrying on for now.")

    async def on_ready(self):
        """ Handles the bot being ready for action."""
        modules = self.config.get_modules()
        logger.info("Loading bot with the following modules loaded: %s", ', '.join(list(map(
            lambda m: m['name'], modules
        ))))

        for module in modules:
            logger.debug("Loading module %(name)s (%(path)s)", module)
            # Build module and register some properties on it.
            Mod: type = import_module(module['path'])
            mod: ModuleBase = getattr(Mod, module['name'])()
            mod.client = self
            mod.eventhandler = self.eventhandler

            # Register it with the core.
            self.modules[module['name']] = mod

            logger.debug("Registering hooks...")
            # Register events.
            mod.register()

        logger.info("Client is ready and listening")

    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        """ React to users adding reactions to messages. """
        if self.eventhandler:
            event = EventFactory.create('reaction', ('add', reaction, user))
            await self.eventhandler.handle(event)
        else:
            logger.warning("No event handler registered... somehow, carrying on for now.")

    def run(self):
        logger.info("Starting up")
        super().run(self.config.get_token())
