""" Base event type. """

class EventBase:

    """ Common event base for all events. """

    body = None
    actual = None
    type = None

    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def get(cls, data):
        """ Get an instance of this class. """
        return cls(data)

    @classmethod
    def matches(cls, event_type, data):
        """ Check if this event can handle the incoming event type and data. """
        raise NotImplementedError("Subclasses have to implement this method")
