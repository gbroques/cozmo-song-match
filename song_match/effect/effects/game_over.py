from cozmo.anim import Triggers

from song_match.effect.effect import Effect



class GameOverEffect(Effect):

    async def play(self, is_player: bool = True) -> None:
        """Play the game over effect.

        * Play ``GameOverEffect.wav``
        * Animate Cozmo with :attr:`~cozmo.anim.Triggers.FrustratedByFailureMajor` or
          :attr:`~cozmo.anim.Triggers.DanceMambo` depending upon ``is_player``.
        * Flash the cubes green.

        :keyword is_player: Whether the player or Cozmo played the correct sequence.
        :return: None
        """


        self._sound.play()
        animation = Triggers.FrustratedByFailureMajor if is_player else Triggers.DanceMambo
        if is_player:
            saying = self._song_robot.say_text('I lost')
        else:
            saying = self._song_robot.say_text('I won')
        await saying.wait_for_completed()
        await self._note_cubes.end_of_game_lights()
        self._play_animation(animation, in_parallel=True)
