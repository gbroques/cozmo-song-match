import os
from abc import ABC

from cozmo.anim import AnimationTrigger
from pygame.mixer import Sound

from song_match.config import ROOT_DIR
from song_match.cube import NoteCubes
from song_match.exceptions import InvalidGameEffectSound
from song_match.song_robot import SongRobot


class Effect(ABC):
    """Abstract base class for game effects."""

    def __init__(self, song_robot: SongRobot):
        self._song_robot = song_robot
        self._sound = self.__get_sound(self.__class__.__name__)

    def _play_animation(self, animation_trigger, **kwargs) -> AnimationTrigger:
        return self._song_robot.robot.play_anim_trigger(animation_trigger, **kwargs)


    @property
    def _note_cubes(self):
        return NoteCubes.of(self._song_robot)

    def __get_sound(self, filename: str) -> Sound:
        return Sound(self.__get_sound_path(filename))

    @staticmethod
    def __get_sound_path(filename: str) -> str:
        filename = filename + '.wav'
        path = os.path.join(ROOT_DIR, 'sfx', 'game', filename)
        if not os.path.isfile(path):
            raise InvalidGameEffectSound(filename)
        return path
