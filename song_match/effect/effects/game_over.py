from typing import List
from typing import Tuple

from cozmo.anim import AnimationTrigger
from cozmo.anim import Triggers

from song_match.effect.effect import Effect
from song_match.player import Player
from song_match.sound_effects import play_collect_point_sound


class GameOverEffect(Effect):

    async def play(self, winners: List[Player], did_cozmo_win: bool = True) -> AnimationTrigger:
        """Play the game over effect.

        * Play ``collect-point.wav``
        * Animate Cozmo with :attr:`~cozmo.anim.Triggers.MajorFail` or
          :attr:`~cozmo.anim.Triggers.DanceMambo` depending upon ``is_cozmo``.
        * Flash the victory sequence.

        :param winners: A list of the players that won the game.
        :param did_cozmo_win: Whether or not Cozmo shared the glory of victory.
        :return: None
        """
        play_collect_point_sound()
        animation = Triggers.DanceMambo if did_cozmo_win else Triggers.MajorFail
        winner_text = self.__get_winner_text(winners, did_cozmo_win)
        await self._song_robot.say_text(winner_text).wait_for_completed()
        return self._song_robot.play_anim_trigger(animation, in_parallel=True)

    def __get_winner_text(self, winners: List[Player], did_cozmo_win: bool) -> str:
        winner_text = ''
        num_of_winners = len(winners)
        if num_of_winners > 0:
            first_winner, rest_of_winners = self.__split_first_winner(winners)
            winner_text += str(first_winner)
            for winner in rest_of_winners:
                winner_text += ' and ' + str(winner)

        if did_cozmo_win and num_of_winners == 0:
            winner_text += 'I won.'
        elif did_cozmo_win and num_of_winners > 0:
            winner_text += ' and I won.'
        else:  # Cozmo lost
            winner_text += ' won.'
            winner_text += 'I lost.'
        return winner_text

    @staticmethod
    def __split_first_winner(winners: List[Player]) -> Tuple[Player, List[Player]]:
        first_winner = winners[0]
        rest_of_winners = winners[1:]
        return first_winner, rest_of_winners
