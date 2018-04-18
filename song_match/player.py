class Player:
    """Represents a human player."""
    def __init__(self, player_id: int):
        self.id = player_id
        self.num_wrong = 0  # Keep track of the number of wrong notes the player taps

    def __str__(self):
        return 'Player ' + str(self.id)

    def __repr__(self):
        return '<Player {}>'.format(self.id)
