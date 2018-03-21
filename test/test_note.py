import unittest

from exceptions import InvalidNote
from song_match import SongMatch
from song_match.note import Note


class TestNote(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._game = SongMatch()

    def test_raises_invalid_note_exception(self):
        with self.assertRaises(InvalidNote):
            Note('c4')

        with self.assertRaises(InvalidNote):
            Note('J6')

        with self.assertRaises(InvalidNote):
            Note('Ab4')

        with self.assertRaises(InvalidNote):
            Note('C10')


if __name__ == '__main__':
    unittest.main()
