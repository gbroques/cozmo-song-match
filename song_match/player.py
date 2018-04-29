from .game_constants import MAX_STRIKES


class Player:
    """Represents a human player."""

    def __init__(self, player_id: int):
        self.id = player_id
        self.num_wrong = 0  # Keep track of the number of wrong notes the player taps

    @property
    def did_win(self) -> bool:
        """Property for accessing whether the player won the game.

        :return: Whether the player won the game.
        """
        return self.num_wrong < MAX_STRIKES

    def __str__(self):
        return 'Player ' + str(self.id)

    def __repr__(self):
        return '<Player {}>'.format(self.id)
