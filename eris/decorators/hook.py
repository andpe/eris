""" Hook decorator. """
import logging

from eris.decorators import BaseDecorator
from eris.events.hooks import Hook as EventHook

LOGGER = logging.getLogger(__name__)


class Hook(BaseDecorator):

    """ Hook decorator, used for more easily setting up handlers for messages. """

    hook: EventHook = None

    def __init__(self, name: str, event_type: str, contains: str = '', match_criteria: str = 'all'):
        """ Create a hook using this function, can be applied multiple times.

        :param name: Name of the hook, used for documentation purposes and debugging.
        :param event_type: Which type of event this is a hook for (e.g., message)
        :param contains: Possible payload string to filter messages for
        :param match_criteria: Which criteria to match the hook against (any or all)
        """
        self.hook = EventHook(name=name, _type=event_type, contains=contains, match_criteria=match_criteria)

    def __call__(self, func):
        self.hook.callback = func

        if hasattr(func, 'hooks'):
            func.hooks.append(self.hook)
        else:
            func.hooks = [self.hook]

        return func
