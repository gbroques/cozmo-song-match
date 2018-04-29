"""Module containing :class:`~song_match.song.songs.hot_cross_buns.HotCrossBuns`."""

from typing import List

from cozmo.lights import Light

from song_match.cube.lights import ORANGE_LIGHT
from song_match.cube.lights import RED_LIGHT
from song_match.cube.lights import YELLOW_LIGHT
from song_match.song import Song
from song_match.song.note import EIGHTH_NOTE
from song_match.song.note import HALF_NOTE
from song_match.song.note import Note
from song_match.song.note import QUARTER_NOTE

MEDIUM = 5
LONG = 11


class HotCrossBuns(Song):
    """Hot Cross Buns"""

    @property
    def _notes(self) -> List[Note]:
        return [
            Note('B3'),
            Note('A3'),
            Note('G3')
        ]

    @property
    def _sequence(self) -> List[Note]:
        a_eighth = Note('A3', EIGHTH_NOTE)
        g_eighth = Note('G3', EIGHTH_NOTE)
        b_quarter = Note('B3', QUARTER_NOTE)
        a_quarter = Note('A3', QUARTER_NOTE)
        g_half = Note('G3', HALF_NOTE)

        return [
            b_quarter, a_quarter, g_half,
            b_quarter, a_quarter, g_half,
            g_eighth, g_eighth, g_eighth, g_eighth,
            a_eighth, a_eighth, a_eighth, a_eighth,
            b_quarter, a_quarter, g_half,

        ]

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
