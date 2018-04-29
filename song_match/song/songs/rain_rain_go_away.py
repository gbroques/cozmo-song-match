"""Module containing :class:`~song_match.song.songs.rain_rain_go_away.RainRainGoAway`."""

from typing import List

from cozmo.lights import Light

from song_match.cube.lights import ORANGE_LIGHT
from song_match.cube.lights import RED_LIGHT
from song_match.cube.lights import YELLOW_LIGHT
from song_match.song import Song
from song_match.song.note import HALF_NOTE
from song_match.song.note import Note

MEDIUM = 8
LONG = 16


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
        g_quarter = Note('G5')
        e_quarter = Note('E5')
        a_quarter = Note('A5')
        g_half = Note('G5', HALF_NOTE)
        e_half = Note('E5', HALF_NOTE)
        return [g_half, e_half,
                g_quarter, g_quarter, e_half,
                g_quarter, g_quarter, e_quarter, a_quarter, g_quarter, g_quarter, e_half,
                g_quarter, e_half,
                g_quarter, g_quarter, e_half,
                g_quarter, g_quarter, e_quarter, a_quarter, g_quarter, g_quarter, e_half]

    @property
    def _cube_lights(self) -> List[Light]:
        return [
            RED_LIGHT,
            ORANGE_LIGHT,
            YELLOW_LIGHT
        ]

    @property
    def _difficulty_markers(self) -> List[int]:
        return [
            MEDIUM,
            LONG
        ]
