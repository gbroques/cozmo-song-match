class InvalidNote(ValueError):
    """Raise if an invalid note occurs."""

    def __init__(self, note):
        message = self._message(note)
        super(InvalidNote, self).__init__(message)

    @staticmethod
    def _message(note: str) -> str:
        return 'Invalid note "' + note + '".'


class MixerNotInitialized(ValueError):
    """Raise if constructing a :class:`~song_match.song.note.Note` instance before initializing the mixer."""

    def __init__(self):
        message = self._message()
        super(MixerNotInitialized, self).__init__(message)

    @staticmethod
    def _message() -> str:
        return ('Mixer not initialized. Please call Note.init_mixer() ' +
                'before constructing a new Note instance.')


class InvalidEffectType(ValueError):
    """Raise if an invalid effect type occurs."""

    def __init__(self, effect_type):
        message = self._message(effect_type)
        super(InvalidEffectType, self).__init__(message)

    @staticmethod
    def _message(effect_type: str) -> str:
        return 'Invalid effect type "' + effect_type + '".'


class InvalidGameEffectSound(ValueError):
    """Raise if an invalid game effect sound occurs."""

    def __init__(self, game_effect_sound):
        message = self._message(game_effect_sound)
        super(InvalidGameEffectSound, self).__init__(message)

    @staticmethod
    def _message(game_effect_sound: str) -> str:
        return 'Invalid game effect sound "' + game_effect_sound + '".'
