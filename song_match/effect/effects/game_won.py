from cozmo.anim import Triggers

from song_match.effect.effect import Effect

class GameWonEffect(Effect):

    async def play(self, is_player: bool = True) -> None:
        """Play the correct sequence effect.

        * Play ``GameWonEffect.wav``
        * Animate Cozmo with :attr:`~cozmo.anim.Triggers.FrustratedByFailureMajor` or
          :attr:`~cozmo.anim.Triggers.DanceMambo` depending upon ``is_player``.
        * Flash the cubes green.

        :keyword is_player: Whether the player or Cozmo played the correct sequence.
        :return: None
        """
        animation = Triggers.FrustratedByFailureMajor if is_player else Triggers.DanceMambo
        if is_player:
            await self._song_robot.cozmo_lose()
        else:
            await self._song_robot.cozmo_win()
        self._sound.play()
        await self._note_cubes.flash_lights_green()
        action = self._play_animation(animation, in_parallel=True)
        await action.wait_for_completed()
