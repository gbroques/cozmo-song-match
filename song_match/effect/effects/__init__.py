"""Package containing various game effects.

  * :class:`~song_match.effect.effects.correct_sequence.CorrectSequenceEffect`
    - Played when a player matches the correct notes.
  * :class:`~song_match.effect.effects.round_transition.RoundTransitionEffect`
    - Played when transitioning between game rounds.
  * :class:`~song_match.effect.effects.wrong_note.WrongNoteEffect`
    - Played when a player fails to match the correct notes.
"""

from .correct_sequence import CorrectSequenceEffect
from .round_transition import RoundTransitionEffect
from .wrong_note import WrongNoteEffect
from .game_over import GameOverEffect
