""" Decorator module.

Contains various decorators for hook callbacks.
"""


class BaseDecorator:

    """ Base class for decorators in Eris. """

    # The interface for hooks means that events will always be the first argument, anything else
    # will be passed as payloads for the events.
    _EVENT_OFFSET: int = 1
