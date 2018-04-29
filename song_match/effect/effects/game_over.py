from typing import List
from typing import Tuple

from cozmo.anim import Triggers

from song_match.effect.effect import Effect
from song_match.player import Player


class GameOverEffect(Effect):

    async def play(self, winners: List[Player], did_cozmo_win: bool = True) -> None:
        """Play the game over effect.

        * Play ``GameOverEffect.wav``
        * Animate Cozmo with :attr:`~cozmo.anim.Triggers.MajorFail` or
          :attr:`~cozmo.anim.Triggers.DanceMambo` depending upon ``is_cozmo``.
        * Flash the victory sequence.

        :param winners: A list of the players that won the game.
        :param did_cozmo_win: Whether or not Cozmo shared the glory of victory.
        :return: None
        """
        self._sound.play()
        animation = Triggers.DanceMambo if did_cozmo_win else Triggers.MajorFail
        winner_text = self.__get_winner_text(winners, did_cozmo_win)
        saying = self._song_robot.say_text(winner_text)
        await saying.wait_for_completed()
        await self._note_cubes.end_of_game_lights()
        self._play_animation(animation, in_parallel=True)

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
