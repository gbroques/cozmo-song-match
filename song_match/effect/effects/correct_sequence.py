from cozmo.anim import Triggers

from song_match.effect.effect import Effect


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
