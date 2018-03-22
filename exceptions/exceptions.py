class InvalidNote(ValueError):
    """Raise if an invalid note occurs."""

    def __init__(self, note):
        message = self._message(note)
        super(InvalidNote, self).__init__(message)

    @staticmethod
    def _message(note: str) -> str:
        return ('Invalid note "' + note + '". ' +
                'Please make sure "' + note + '" corresponds ' +
                'to a .wav file in "sfx/piano/".')


class MixerNotInitialized(ValueError):
    """Raise if constructing a Note instance before initializing the mixer."""

    def __init__(self):
        message = self._message()
        super(MixerNotInitialized, self).__init__(message)

    @staticmethod
    def _message() -> str:
        return ('Mixer not initialized. Please call Note.init_mixer() ' +
                'before constructing a new Note instance.')
