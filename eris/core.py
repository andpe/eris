""" Main module for the discord bot. """
import json
import logging
from importlib import import_module
from types import ModuleType
from typing import Union, Type

import discord

from eris.config import Config
from eris.decorators.admin import AdminOnly
from eris.events.factory import EventFactory
from eris.events.handler import EventHandler

logging.basicConfig()
LOGGER = logging.getLogger(__name__)


class Core(discord.Client):
    """ Main class for handling the bot logic.

    Handles loading modules and routing events to the event handler.
    """

    eventhandler = None
    config = None
    modules = None

    def __init__(self, config: Union[str, dict, Config], *args, config_cls: Type[Config] = Config, **kwargs):
        """ Create a new bot with the specified config.

        Parameters
        --------
        config:
            The configuration to use when starting up the bot.

            This can be either a string (a path to a file to load), a dictionary or a Config instance (or subclass).
            Dicts must be valid according to config_cls (which is :class:`Config` by default.
        config_cls:
            The configuration class to use when instantiating the config (if a Config or sublcass of it is not passed).

        args:
            This gets passed on to discord.py

        kwargs:
            This gets passed on to discord.py

        """
        self.eventhandler = EventHandler()
        self.modules = {}

        if isinstance(config, str):
            # Load the configuration and validate it.
            with open(config, 'r') as configfile:
                cfg = json.load(configfile)

            self.config = config_cls.parse_obj(cfg)
        elif isinstance(config, Config):
            self.config = config
        elif isinstance(config, dict) and config_cls:
            self.config = config_cls.parse_obj(config)
        else:
            raise TypeError("config should be of either an instance/sublcass of eris.Config "
                            "(or a dict compatible with it)"
                            )

        AdminOnly.register_config(self.config)
        EventFactory.init()

        # Carry on as normal.
        super().__init__(*args, **kwargs)

    async def on_message(self, message):
        """ Handles incoming messages from discord.py. """
        if not self.is_ready():
            LOGGER.warning("Ignored event that arrived before we were ready.")
            return

        if self.eventhandler:
            event = EventFactory.create('message', message)
            await self.eventhandler.handle(event)
        else:
            LOGGER.warning("No eventhandler registered... somehow, carrying on for now.")

    async def on_ready(self):
        """ Handles the bot being ready for action."""
        for guild in self.guilds:
            LOGGER.info("Joined %s (%d)", guild.name, guild.id)

        LOGGER.info("Client is ready and listening")

    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState,
                                    after: discord.VoiceState):
        """ React to users changing their voice states. """
        if not self.is_ready():
            LOGGER.warning("Ignored event that arrived before we were ready.")
            return

        if self.eventhandler:
            event = EventFactory.create('voicestate', (member, before, after))
            await self.eventhandler.handle(event)
        else:
            LOGGER.warning("No event handler registered... somehow, carrying on for now.")

    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        """ React to users adding reactions to messages. """
        if not self.is_ready():
            LOGGER.warning("Ignored event that arrived before we were ready.")
            return

        if self.eventhandler:
            event = EventFactory.create('reaction', ('add', reaction, user))
            await self.eventhandler.handle(event)
        else:
            LOGGER.warning("No event handler registered... somehow, carrying on for now.")

    def run(self, *args, **kwargs):
        """ Run some bootstrap stuff and then run the main bot. """
        LOGGER.info("Starting up")

        self._load_modules()

        super().run(
            *((self.config.get_token(),) + args),
            **kwargs
        )

    def _load_modules(self):
        """ Load the modules that have been enabled in the configuration. """
        # We import this here to avoid a cyclic import from ruining our day.
        # pylint: disable=C0415,R0401
        from eris.modules.base import GenericModuleBase
        modules = self.config.get_modules()
        LOGGER.info("Loading bot with the following modules loaded: %s", ', '.join(list(map(
            lambda m: m.name, modules
        ))))
        for module in modules:
            LOGGER.debug("Loading module %(name)s (%(path)s)", module)
            # Build module and register some properties on it.
            modcls: ModuleType = import_module(module.path)
            mod: GenericModuleBase[Core] = getattr(modcls, module.name)()
            mod.client = self
            mod.eventhandler = self.eventhandler

            # Register it with the core.
            self.modules[module.name] = mod

            LOGGER.debug("Registering hooks...")
            # Register events and scan for hook decorators.
            mod.register()
            mod.scan_decorators()
