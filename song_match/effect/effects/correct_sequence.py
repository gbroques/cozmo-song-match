from cozmo.anim import Triggers

from song_match.effect.effect import Effect


class CorrectSequenceEffect(Effect):
    """Played when either a player or Cozmo matches a sequence of notes correctly."""

    async def play(self, current_position: int, longer_anim_position: int, is_player: bool = True) -> None:
        """Play the correct sequence effect.

        * Play ``CorrectSequenceEffect.wav``
        * Animate Cozmo with :attr:`~cozmo.anim.Triggers.MemoryMatchPlayerWinHand` or
          :attr:`~cozmo.anim.Triggers.MemoryMatchCozmoWinHand` depending upon ``is_player``.
        * Flash the cubes green.

        :keyword is_player: Whether the player or Cozmo played the correct sequence.
        :return: None
        """
        self._sound.play()
        if current_position <= longer_anim_position:
            animation = Triggers.MemoryMatchPlayerWinHand if is_player else Triggers.MemoryMatchCozmoWinHand
        else:
            animation = Triggers.MemoryMatchPlayerWinHandLong if is_player else Triggers.MemoryMatchCozmoWinHandLong

        action = self._play_animation(animation, in_parallel=True)
        await self._note_cubes.flash_lights_green()
        await action.wait_for_completed()
