import unittest
from unittest.mock import patch

from song_match.exceptions import InvalidNote
from song_match.song import Note


class TestNote(unittest.TestCase):

    @patch('song_match.song.note.init')
    def test_raises_invalid_note_exception(self, init):
        Note.init_mixer()
        with self.assertRaises(InvalidNote):
            Note('c4')

        with self.assertRaises(InvalidNote):
            Note('J6')

        with self.assertRaises(InvalidNote):
            Note('Ab4')

        with self.assertRaises(InvalidNote):
            Note('C10')

        assert init.called


if __name__ == '__main__':
    unittest.main()
