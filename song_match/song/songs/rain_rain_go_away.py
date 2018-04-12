"""Module containing :class:`~song_match.song.songs.rain_rain_go_away.RainRainGoAway`."""

from typing import List

from cozmo.lights import Light

from song_match.cube.lights import ORANGE_LIGHT
from song_match.cube.lights import RED_LIGHT
from song_match.cube.lights import YELLOW_LIGHT
from song_match.song import Song
from song_match.song.note import Note


class RainRainGoAway(Song):

    @property
    def _notes(self) -> List[Note]:
        return [
            Note('E5'),
            Note('G5'),
            Note('A5')
        ]

    @property
    def _sequence(self) -> List[Note]:
        e5, g5, a5 = self._notes
        return [g5, e5,
                g5, g5, e5,
                g5, g5, e5, a5, g5, g5, e5,
                g5, e5,
                g5, g5, e5,
                g5, g5, e5, a5, g5, g5, e5]

    @property
    def _cube_lights(self) -> List[Light]:
        return [
            RED_LIGHT,
            ORANGE_LIGHT,
            YELLOW_LIGHT
        ]
