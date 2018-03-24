from abc import ABC, abstractmethod
from typing import List

from cozmo.lights import Light

from song_match.song.note import Note


class Song(ABC):
    """Abstract base class for songs.

    Currently only supports songs with 3 notes.
    """

    def play_note(self, cube_id: int) -> None:
        """Plays a note for a corresponding cube.

        :param cube_id: Cube ID. Possible values include 1, 2, and 3.
        :return None:
        """
        index = self._get_index(cube_id)
        return self._notes[index].play()

    def get_cube_light(self, cube_id: int) -> Light:
        """
        :param cube_id: Cube ID. Possible values include 1, 2, and 3.
        :return: Cube light for the corresponding cube.
        """
        index = self._get_index(cube_id)
        return self._cube_lights[index]

    def get_cube_id(self, note: Note) -> int:
        """Get the Cube ID for a corresponding note.

        :param note: The note of the song.
        :return: Cube ID. Possible values include 1, 2, and 3.
        """
        return self._notes.index(note) + 1

    @staticmethod
    def _get_index(cube_id: int):
        return cube_id - 1

    @property
    @abstractmethod
    def _notes(self) -> List[Note]:
        """Returns a list of 3 notes in ascending order by pitch."""

    @property
    @abstractmethod
    def _sequence(self) -> List[Note]:
        """Returns a sequence of notes that make up the song."""

    @property
    @abstractmethod
    def _cube_lights(self) -> List[Light]:
        """A list of 3 lights for each cube."""
