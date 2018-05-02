"""Module containing :class:`~song_match.song.songs.mary_had_a_little_lamb.MaryHadALittleLamb`."""

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


class MaryHadALittleLamb(Song):
    """Mary Had a Little Lamb"""

    @property
    def _notes(self) -> List[Note]:
        return [
            Note('C4'),
            Note('D4'),
            Note('E4')
        ]

    @property
    def _sequence(self) -> List[Note]:
        c_quarter = Note('C4', QUARTER_NOTE)
        d_quarter = Note('D4', QUARTER_NOTE)
        e_quarter = Note('E4', QUARTER_NOTE)
        d_half = Note('D4', HALF_NOTE)
        e_half = Note('E4', HALF_NOTE)
        return [
            e_quarter, d_quarter, c_quarter, d_quarter, e_quarter,
            e_quarter, e_half, d_quarter, d_quarter, d_half,
            e_quarter, e_quarter, e_half, e_quarter, d_quarter,
            c_quarter, d_quarter, e_quarter, e_quarter, e_half,
            d_quarter, d_quarter, e_quarter, d_quarter, c_quarter,
        ]

    @property
    def _cube_lights(self) -> List[Light]:
        return [
            PINK_LIGHT,
            BLUE_LIGHT,
            CYAN_LIGHT
        ]

    @property
    def _difficulty_markers(self) -> List[int]:
        return [
            MEDIUM,
            LONG
        ]
