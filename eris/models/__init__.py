""" A module for various models in the codebase. """
import pydantic


class ModuleConfig(pydantic.BaseModel):
    """ A model for how a module configuration should look. """
    name: str
    path: str
