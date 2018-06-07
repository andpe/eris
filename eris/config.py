""" Configuration class for the eris. """
import jsonschema


class Config:

    """ Configuration class for the eris. """
    version = 1

    schema = {
        "description": "Representation of a configuration file for Eris.",
        "type": "object",
        "required": ["modules", "token"],
        "properties": {
            "modules": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "path": {"type": "string", "pattern": "^([a-zA-Z0-9_.])+$"}
                    },
                    "required": ["name", "path"]
                }
            }
        }
    }

    config = None

    def __init__(self, config):
        self.config = config

        # If this fails we should probably just die from it so that it can be handled by someone that knows how to
        # handle it.
        jsonschema.validate(config, self.schema)

    def get_modules(self) -> list:
        """ Return a list of modules in this configuration. """
        return self.config['modules']

    def get_token(self) -> str:
        return self.config['token']

    def __getitem__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]
        else:
            return self.config[item]