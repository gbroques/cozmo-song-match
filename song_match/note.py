from os.path import isfile, join

from pygame.mixer import Sound

from config import ROOT_DIR
from exceptions import InvalidNote


class Note:
    def __init__(self, note: str):
        self._note = note
        self._sound = Sound(self._get_sound_path())

    def play(self):
        self._sound.play()

    def _get_sound_path(self) -> str:
        filename = self._note + '.wav'
        path = join(ROOT_DIR, 'sfx', 'piano', filename)
        if not isfile(path):
            raise InvalidNote(self._note)
        return path
