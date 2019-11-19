""" Main module for the discord bot. """
import logging
from importlib import import_module

import discord

from eris.config import Config
from eris.decorators.admin import AdminOnly
from eris.events.factory import EventFactory
from eris.events.handler import EventHandler
from eris.modules.base import ModuleBase

logging.basicConfig()
LOGGER = logging.getLogger(__name__)


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
        with open(config, 'r') as configfile:
            import json
            cfg = json.load(configfile)
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
            LOGGER.warning("No eventhandler registered... somehow, carrying on for now.")

    async def on_ready(self):
        """ Handles the bot being ready for action."""
        modules = self.config.get_modules()
        LOGGER.info("Loading bot with the following modules loaded: %s", ', '.join(list(map(
            lambda m: m['name'], modules
        ))))

        for module in modules:
            LOGGER.debug("Loading module %(name)s (%(path)s)", module)
            # Build module and register some properties on it.
            modcls: type = import_module(module['path'])
            mod: ModuleBase = getattr(modcls, module['name'])()
            mod.client = self
            mod.eventhandler = self.eventhandler

            # Register it with the core.
            self.modules[module['name']] = mod

            LOGGER.debug("Registering hooks...")
            # Register events.
            mod.register()

        LOGGER.info("Client is ready and listening")

    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        """ React to users changing their voice states. """
        if self.eventhandler:
            event = EventFactory.create('voicestate', (member, before, after))
            await self.eventhandler.handle(event)
        else:
            LOGGER.warning("No event handler registered... somehow, carrying on for now.")

    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        """ React to users adding reactions to messages. """
        if self.eventhandler:
            event = EventFactory.create('reaction', ('add', reaction, user))
            await self.eventhandler.handle(event)
        else:
            LOGGER.warning("No event handler registered... somehow, carrying on for now.")

    def run(self, *args, **kwargs):
        LOGGER.info("Starting up")
        super().run(
            *((self.config.get_token(),) + args),
            **kwargs
        )
