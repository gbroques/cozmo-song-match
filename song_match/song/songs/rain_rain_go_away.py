"""Module containing :class:`~song_match.song.songs.rain_rain_go_away.RainRainGoAway`."""

from typing import List

from cozmo.lights import Light

from song_match.cube.lights import BLUE_LIGHT
from song_match.cube.lights import CYAN_LIGHT
from song_match.cube.lights import PINK_LIGHT
from song_match.song import Song
from song_match.song.note import HALF_NOTE
from song_match.song.note import Note
from song_match.song.note import QUARTER_NOTE

MEDIUM = 8
LONG = 16


class RainRainGoAway(Song):
    """Rain Rain Go Away"""

    @property
    def _notes(self) -> List[Note]:
        return [
            Note('E5'),
            Note('G5'),
            Note('A5')
        ]

    @property
    def _sequence(self) -> List[Note]:
        g_quarter = Note('G5', QUARTER_NOTE)
        e_quarter = Note('E5', QUARTER_NOTE)
        a_quarter = Note('A5', QUARTER_NOTE)
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
            BLUE_LIGHT,
            PINK_LIGHT,
            CYAN_LIGHT
        ]

    @property
    def _difficulty_markers(self) -> List[int]:
        return [
            MEDIUM,
            LONG
        ]
