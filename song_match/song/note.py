"""Module containing :class:`~song_match.song.note.Note`."""

from pygame.mixer import Sound

from song_match.sound_effects import get_piano_note_sound_path

# TODO: Make relative off a single base duration
EIGHTH_NOTE = .2  #: Time for eighth note.
QUARTER_NOTE = .4  #: Time for quarter note.
HALF_NOTE = .8  #: Time for half note.
WHOLE_NOTE = 1.6  #: Time for whole note.


class Note:
    """Represents a musical note."""

    def __init__(self, note: str, duration: int = QUARTER_NOTE):
        self.duration = duration
        self.note = note
        self.__sound = Sound(get_piano_note_sound_path(note))

    def play(self) -> None:
        """Play the note.

        :return: None
        """
        self.__sound.play()

    def __eq__(self, other):
        return isinstance(other, Note) and self.note == other.note

    def __repr__(self):
        return "<Note '{}'>".format(self.note)

    def __str__(self):
        return "<Note '{}'>".format(self.note)
