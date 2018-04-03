"""Module containing :class:`~song_match.cube.note_cubes.NoteCubes`."""

from typing import List

from cozmo.objects import LightCube

from song_match.song import Song
from .note_cube import NoteCube


class NoteCubes:
    """Container class for three :class:`~cozmo.objects.LightCube` instances."""

    def __init__(self, cubes: List[LightCube], song: Song):
        self._cubes = cubes
        self._song = song

    def turn_on_lights(self) -> None:
        """Turn on the light for each note cube.

        :return: None
        """
        for cube in self._cubes:
            note_cube = NoteCube(cube, self._song)
            note_cube.turn_on_light()
