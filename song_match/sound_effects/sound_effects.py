import os

from pygame.mixer import Sound

from song_match.config import ROOT_DIR
from song_match.exceptions import InvalidGameEffectSound
from song_match.exceptions import InvalidNote

# Game sounds
COLLECT_POINT = 'collect-point'
LEVEL_COMPLETE = 'level-complete'
WRONG_BUZZER = 'wrong-buzzer'

# Sound effect packages
GAME = 'game'
PIANO = 'piano'


def get_collect_point_sound() -> Sound:
    """Get the collect point sound.

    :return: :class:`~pygame.mixer.Sound`
    """
    return Sound(__get_game_sound_path(COLLECT_POINT))


def get_level_complete_sound() -> Sound:
    """Get the level complete sound.

    :return: :class:`~pygame.mixer.Sound`
    """
    return Sound(__get_game_sound_path(LEVEL_COMPLETE))


def get_wrong_buzzer_sound() -> Sound:
    """Get the wrong buzzer sound.

    :return: :class:`~pygame.mixer.Sound`
    """
    return Sound(__get_game_sound_path(WRONG_BUZZER))


def play_collect_point_sound() -> None:
    """Play ``collect-point.wav``.

    :return: None
    """
    get_collect_point_sound().play()


def play_level_complete_sound() -> None:
    """Play ``level-complete.wav``.

    :return: None
    """
    get_level_complete_sound().play()


def play_wrong_buzzer_sound() -> None:
    """Play ``wrong-buzzer.wav``.

    :return: None
    """
    get_wrong_buzzer_sound().play()


def get_piano_note_sound_path(name: str) -> str:
    """Get the path to a piano note sound file.

    :param name: The name of the note. For example, C4.
    :return: The path to a piano note sound.
    """
    return __get_sound_path(name, PIANO)


def __get_game_sound_path(name: str) -> str:
    return __get_sound_path(name, GAME)


def __get_sound_path(name: str, sound_effect_package: str) -> str:
    filename = name + '.wav'
    path = os.path.join(ROOT_DIR, 'sound_effects', sound_effect_package, filename)
    if not os.path.isfile(path):
        if sound_effect_package == GAME:
            raise InvalidGameEffectSound(name)
        elif sound_effect_package == PIANO:
            raise InvalidNote(name)
        else:
            raise ValueError('Invalid file {}'.format(filename))
    return path
