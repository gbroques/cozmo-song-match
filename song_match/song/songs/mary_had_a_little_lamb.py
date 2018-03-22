from typing import List

from cozmo.lights import Light

from song_match.cube.lights import ORANGE_LIGHT
from song_match.cube.lights import RED_LIGHT
from song_match.cube.lights import YELLOW_LIGHT
from song_match.song import Song
from song_match.song.note import Note


class MaryHadALittleLamb(Song):

    @property
    def _notes(self) -> List[Note]:
        return [
            Note('C4'),
            Note('D4'),
            Note('E4')
        ]

    @property
    def _sequence(self) -> List[Note]:
        c4, d4, e4 = self._notes
        return [
            e4, d4, c4, d4, e4,
            e4, e4, d4, d4, d4,
            e4, e4, e4, e4, d4,
            c4, d4, e4, e4, e4,
            d4, d4, e4, d4, c4,
        ]

    @property
    def _cube_lights(self) -> List[Light]:
        return [
            RED_LIGHT,
            ORANGE_LIGHT,
            YELLOW_LIGHT
        ]
