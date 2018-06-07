class EventBase(object):
    body = None
    actual = None
    type = None

    @classmethod
    def get(cls, data):
        return cls(data)

    @classmethod
    def matches(cls, type, data):
        raise NotImplementedError("Subclasses have to implement this method")