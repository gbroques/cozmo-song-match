from song_match.exceptions import InvalidEffectType
from song_match.song_robot import SongRobot
from .effects import CorrectSequenceEffect
from .effects import RoundTransitionEffect
from .effects import WrongNoteEffect
from .effects import GameOverEffect

class EffectFactory:
    """Factory for creating :class:`~song_match.effect.effect.Effect` instances."""

    def __init__(self, song_robot: SongRobot):
        self._song_robot = song_robot

    def create(self, effect_type: str):
        """Factory method for creating effects.

        Usage: :code:`create('WrongNote')`

        :param effect_type: Upper camel case class name of the effect.
        :return: :class:`~song_match.effect.effect.Effect`
        """
        if effect_type == 'CorrectSequence':
            return CorrectSequenceEffect(self._song_robot)
        elif effect_type == 'WrongNote':
            return WrongNoteEffect(self._song_robot)
        elif effect_type == 'RoundTransition':
            return RoundTransitionEffect(self._song_robot)
        elif effect_type == 'GameOver':
            return GameOverEffect(self._song_robot)
        else:
            raise InvalidEffectType(effect_type)
