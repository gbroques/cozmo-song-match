import os
from abc import ABC
from asyncio import sleep

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
        elif effect_type == 'RoundTransition':
            return RoundTransitionEffect(self._song_robot)


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

    async def play(self, cube_id: int, is_player: bool = True) -> None:
        """Play the wrong note effect.

        * Play ``WrongNoteEffect.wav``
        * Animate Cozmo with :attr:`~cozmo.anim.Triggers.MemoryMatchPlayerLoseHand` or
          :attr:`~cozmo.anim.Triggers.MemoryMatchCozmoLoseHand` depending upon ``is_player``.
        * Flash the incorrect cube red.

        :param cube_id: :attr:`~cozmo.objects.LightCube.cube_id`
        :param is_player: Whether the player or Cozmo played the wrong note.
        :return: None
        """
        self._sound.play()
        animation = Triggers.MemoryMatchPlayerLoseHand if is_player else Triggers.MemoryMatchCozmoLoseHand
        action = self._play_animation(animation, in_parallel=True)
        await self._note_cubes.flash_single_cube_red(cube_id)
        await action.wait_for_completed()


class CorrectSequenceEffect(Effect):

    async def play(self, is_player: bool = True) -> None:
        """Play the correct sequence effect.

        * Play ``CorrectSequenceEffect.wav``
        * Animate Cozmo with :attr:`~cozmo.anim.Triggers.MemoryMatchPlayerWinHand` or
          :attr:`~cozmo.anim.Triggers.MemoryMatchCozmoWinHand` depending upon ``is_player``.
        * Flash the cubes green.

        :keyword is_player: Whether the player or Cozmo played the correct sequence.
        :return: None
        """
        self._sound.play()
        animation = Triggers.MemoryMatchPlayerWinHand if is_player else Triggers.MemoryMatchCozmoWinHand
        action = self._play_animation(animation, in_parallel=True)
        await self._note_cubes.flash_lights_green()
        await action.wait_for_completed()


class RoundTransitionEffect(Effect):

    async def play(self) -> None:
        """Play the round transition effect.

        * Play ``RoundTransitionEffect.wav``.
        * Start the light chaser effect on each cube.

        :return: None
        """
        self._sound.play()
        await self._song_robot.turn_back_to_center(in_parallel=True)
        await self._note_cubes.start_light_chasers()
        await sleep(1)
