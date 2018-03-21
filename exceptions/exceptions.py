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
