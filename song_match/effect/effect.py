from abc import ABC

from song_match.cube import NoteCubes
from song_match.song_robot import SongRobot


class Effect(ABC):
    """Abstract base class for game effects."""

    def __init__(self, song_robot: SongRobot):
        self._song_robot = song_robot

    @property
    def _note_cubes(self):
        return NoteCubes.of(self._song_robot)
