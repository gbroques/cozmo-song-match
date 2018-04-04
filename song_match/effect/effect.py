import os
from abc import ABC

from cozmo.anim import Triggers, AnimationTrigger
from pygame.mixer import Sound

from song_match.config import ROOT_DIR
from song_match.cube import NoteCubes
from song_match.song_robot import SongRobot


class EffectFactory:
    """Factory for creating :class:`~song_match.effect.effect.Effect` instances."""

    def __init__(self, song_robot: SongRobot):
        self._song_robot = song_robot

    def create(self, effect_type: str):
        """Factory method for creating effects.

        Usage: :code:`create('WrongNote')`

        :param effect_type: Camel case class name of the effect.
        :return: :class:`~song_match.effect.effect.Effect`
        """
        if effect_type == 'WrongNote':
            return WrongNoteEffect(self._song_robot)
        elif effect_type == 'CorrectSequence':
            return CorrectSequenceEffect(self._song_robot)


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
        return os.path.join(ROOT_DIR, 'sfx', 'game', filename)


class WrongNoteEffect(Effect):

    async def play(self, cube_id: int) -> None:
        """Play the wrong note effect.

        * Play ``WrongNoteEffect.wav``
        * Animate Cozmo with :attr:`~cozmo.anim.Triggers.MemoryMatchPlayerLoseHand`.
        * Flash the incorrect cube red.

        :param cube_id: :attr:`~cozmo.objects.LightCube.cube_id`
        :return: None
        """
        self._sound.play()
        action = self._play_animation(Triggers.MemoryMatchPlayerLoseHand, in_parallel=True)
        await self._note_cubes.flash_single_cube_red(cube_id)
        await action.wait_for_completed()


class CorrectSequenceEffect(Effect):

    async def play(self) -> None:
        """Play the correct sequence effect.

        * Play ``CorrectSequenceEffect.wav``
        * Animate Cozmo with :attr:`~cozmo.anim.Triggers.MemoryMatchPlayerWinHandSolo`.
        * Flash the cubes green.

        :return: None
        """
        self._sound.play()
        action = self._play_animation(Triggers.MemoryMatchPlayerWinHandSolo, in_parallel=True)
        await self._note_cubes.flash_lights_green()
        await action.wait_for_completed()
