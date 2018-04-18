"""Module containing :class:`~song_match.song.songs.mary_had_a_little_lamb.MaryHadALittleLamb`."""

from typing import List

from cozmo.lights import Light

from song_match.cube.lights import ORANGE_LIGHT
from song_match.cube.lights import RED_LIGHT
from song_match.cube.lights import YELLOW_LIGHT
from song_match.song import Song
from song_match.song.note import Note

EIGHTH_NOTE = .25 # time for eighth note
QUARTER_NOTE = .5 # time for quarter note
HALF_NOTE = 1 # time half note
WHOLE_NOTE = 2 # time for whole note

class MaryHadALittleLamb(Song):

    @property
    def _notes(self) -> List[Note]:
        return [
            Note('C4', HALF_NOTE),
            Note('D4', HALF_NOTE),
            Note('E4', HALF_NOTE)
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
            RED_LIGHT,
            ORANGE_LIGHT,
            YELLOW_LIGHT
        ]
