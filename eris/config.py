""" Configuration class for the eris. """
from typing import List

import pydantic

from eris.models import ModuleConfig


class Config(pydantic.BaseModel):

    """ Configuration class for the eris. """

    modules: List[ModuleConfig] = []
    token: str

    def get_modules(self) -> List[ModuleConfig]:
        """ Return a list of modules in this configuration. """
        return self.modules

    def get_token(self) -> str:
        """ Get the bot token. """
        return self.token