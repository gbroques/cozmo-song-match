from song_match.song import Song
from .note_cube import NoteCube


class NoteCubes:
    """Container class for the three note cubes."""

    def __init__(self, cubes, song: Song):
        self._cubes = cubes
        self._song = song

    def turn_on_lights(self) -> None:
        """Turn on the light for each note cube."""
        for cube in self._cubes:
            note_cube = NoteCube(cube, self._song)
            note_cube.turn_on_light()
