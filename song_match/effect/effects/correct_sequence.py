from cozmo.anim import Triggers

from song_match.effect.effect import Effect
from song_match.sound_effects import play_collect_point_sound


class CorrectSequenceEffect(Effect):
    """Played when either a player or Cozmo matches a sequence of notes correctly."""

    async def play(self, is_sequence_long: bool = False, is_player: bool = True) -> None:
        """Play the correct sequence effect.

        * Play ``collect-point.wav``
        * Animate Cozmo with :attr:`~cozmo.anim.Triggers.MemoryMatchPlayerWinHand` or
          :attr:`~cozmo.anim.Triggers.MemoryMatchCozmoWinHand` depending upon ``is_player``.
        * Flash the cubes green.

        :keyword is_sequence_long: Whether the sequence the player matched was long.
        :keyword is_player: Whether the player or Cozmo played the correct sequence.
        :return: None
        """
        play_collect_point_sound()
        animation = self.__get_animation(is_sequence_long, is_player)
        action = self._song_robot.play_anim_trigger(animation, in_parallel=True)
        await self._note_cubes.flash_lights_green()
        await action.wait_for_completed()

    @staticmethod
    def __get_animation(is_sequence_long: bool, is_player: bool) -> Triggers:
        if is_sequence_long and is_player:
            return Triggers.MemoryMatchPlayerWinHandLong
        else:
            if is_player:
                return Triggers.MemoryMatchPlayerWinHand
            else:
                return Triggers.MemoryMatchCozmoWinHand
