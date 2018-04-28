from cozmo.anim import Triggers

from song_match.effect.effect import Effect



class GameOverEffect(Effect):

    async def play(self, winners, is_cozmo: bool = True) -> None:
        """Play the game over effect.

        * Play ``GameOverEffect.wav``
        * Animate Cozmo with :attr:`~cozmo.anim.Triggers.FrustratedByFailureMajor` or
          :attr:`~cozmo.anim.Triggers.DanceMambo` depending upon ``is_cozmo``.
        * Flash the victory sequence.

        :keyword is_cozmo: Whether or not Cozmo shared the glory of victory.
        :return: None
        """

        self._sound.play()
        animation = Triggers.DanceMambo if is_cozmo else Triggers.FrustratedByFailureMajor
        saying = self._song_robot.say_text(winners)
        await saying.wait_for_completed()
        await self._note_cubes.end_of_game_lights()
        self._play_animation(animation, in_parallel=True)
