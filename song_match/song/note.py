from os.path import isfile, join

from pygame.mixer import init, Sound

from config import ROOT_DIR
from exceptions import InvalidNote
from exceptions import MixerNotInitialized


class Note:
    __is_mixer_initialized = False

    def __init__(self, note: str):
        """Construct a new Note.
        The note is case-sensitive and must match a .wav file.
        Note.mixer_init() must be called before constructing any Note instances.
        :param note: Must be a valid note .wav filename. For example, C4 or A#2.
        """
        if not self.__is_mixer_initialized:
            raise MixerNotInitialized()

        self.note = note
        self.__sound = Sound(self.__get_sound_path())

    @classmethod
    def init_mixer(cls):
        """Initializes pygame's mixer module.
        Must be called before constructing any Note objects.
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
        path = join(ROOT_DIR, 'sfx', 'piano', filename)
        if not isfile(path):
            raise InvalidNote(self.note)
        return path

    def __eq__(self, other):
        return isinstance(other, Note) and self.note == other.note
