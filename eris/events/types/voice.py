""" Voice state event. """
import discord

from eris.events.types.eventbase import EventBase


class VoiceStateEvent(EventBase):
    """ Class for handling voice state changes. """

    member: discord.Member = None
    before: discord.VoiceState = None
    after: discord.VoiceState = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.member, self.before, self.after = args[0]
        self.type = 'voicestate'

    @classmethod
    def matches(cls, event_type, data):
        if event_type == 'voicestate' and len(data) > 1:
            return isinstance(data[0], discord.Member) and \
                   isinstance(data[1], discord.VoiceState) and \
                   isinstance(data[2], discord.VoiceState)

        return False
