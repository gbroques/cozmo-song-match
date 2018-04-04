"""Module containing :class:`~song_match.song.note.Note`."""

import os

from pygame.mixer import init, Sound

from song_match.config import ROOT_DIR
from song_match.exceptions import InvalidNote
from song_match.exceptions import MixerNotInitialized


class Note:
    __is_mixer_initialized = False

    def __init__(self, note: str):
        if not self.__is_mixer_initialized:
            raise MixerNotInitialized()

        self.note = note
        self.__sound = Sound(self.__get_sound_path())

    @classmethod
    def init_mixer(cls) -> None:
        """Initializes pygame's mixer module.

        See https://www.pygame.org/docs/ref/mixer.html#pygame.mixer.init.

        **IMPORTANT:** Must be called before constructing any :class:`~song_match.song.note.Note` objects.

        :return: None
        """
        cls.__is_mixer_initialized = True
        init(frequency=44100, size=-16, channels=1, buffer=1024)

    def play(self) -> None:
        """Play the note.

        :return: None
        """
        self.__sound.play()

    def __get_sound_path(self) -> str:
        filename = self.note + '.wav'
        path = os.path.join(ROOT_DIR, 'sfx', 'piano', filename)
        if not os.path.isfile(path):
            raise InvalidNote(self.note)
        return path

    def __eq__(self, other):
        return isinstance(other, Note) and self.note == other.note

    def __repr__(self):
        return "<Note '{}'>".format(self.note)

    def __str__(self):
        return "<Note '{}'>".format(self.note)
