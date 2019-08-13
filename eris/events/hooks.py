from eris.events.types.eventbase import EventBase

HOOK_EAT_NONE = 0
HOOK_EAT_PRIO = 1
HOOK_EAT_MODULE = 2
HOOK_EAT_SYSTEM = 4
HOOK_EAT_ALL = HOOK_EAT_NONE | HOOK_EAT_PRIO | HOOK_EAT_MODULE | HOOK_EAT_SYSTEM


class Hook:
    """ Hook object used by the EventHandler to filter events and call the appropriate functions on modules. """

    name: str = None
    type: str = None
    contains: str = None
    match_criteria: str = 'all'
    callback: callable = None

    def __init__(self, name: str, type: str, callback: callable = None, contains: str = None,
                 match_criteria: str = 'all'):
        """ Create a new hook.

        :param name: Name of the hook, must be unique for the module.
        :type name: str
        :param type: What type of event this hook will listen for.
        :type type: str
        :param callback: Function to call when a match has been found.
        :type callback: callable
        :param contains: Keyword argument for checking the contents of the event.
        :type contains: str
        :param match_criteria: 'all' for requiring all requirements to match 'any' to be satisified with any.
        :type match_criteria: str
        """
        self.name = name
        self.type = type
        self.callback = callback
        self.contains = contains
        self.match_criteria = match_criteria

    def match(self, event: EventBase) -> bool:
        """ Check if the event matches this hook. """
        # For now there's only one thing to check.
        typematch = event.type == self.type
        if self.contains and event.body:
            contains = self.contains in event.body
        elif self.contains and not event.body:
            contains = False
        else:
            contains = True

        if self.match_criteria == 'all':
            return all([typematch, contains])
        elif self.match_criteria == 'any':
            return any([typematch, contains])

    def call(self, event):
        """ Call the callback for this hook. """
        return self.callback(event)
