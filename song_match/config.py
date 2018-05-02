import os

from pygame.mixer import init

#: Root directory of the package to help load ``.wav`` files.
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def init_mixer() -> None:
    """Initializes pygame's mixer module by calling :func:`~pygame.mixer.init`.

    See https://www.pygame.org/docs/ref/mixer.html#pygame.mixer.init.

    **IMPORTANT:** Must be called before constructing any :class:`~song_match.song.note.Note` objects.

    :return: None
    """
    init(frequency=44100, size=-16, channels=1, buffer=1024)
