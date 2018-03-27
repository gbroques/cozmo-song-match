"""Module containing :class:`~song_match.song.song.Song`."""

from abc import ABC, abstractmethod
from typing import List

from cozmo.lights import Light

from song_match.song.note import Note


class Song(ABC):
    """Abstract base class for songs.

    Currently only supports songs with 3 notes.

    Must override **3** abstract properties:

    1. ``_notes`` - A list of 3 :class:`~song_match.song.note.Note` instances in ascending order by pitch.
    2. ``_sequence`` - A sequence of :class:`~song_match.song.note.Note` instances that make up the song.
    3. ``_cube_lights`` - A list of 3 :class:`~cozmo.lights.Light` instances.
    """

    def play_note(self, cube_id: int) -> None:
        """Plays a note for a corresponding cube.

        :param cube_id: :attr:`~cozmo.objects.LightCube.cube_id`
        :return: None
        """
        index = self._get_index(cube_id)
        return self._notes[index].play()

    def get_cube_light(self, cube_id: int) -> Light:
        """Get the :class:`~cozmo.lights.Light` for a corresponding cube.

        :param cube_id: :attr:`~cozmo.objects.LightCube.cube_id`
        :return: :class:`~cozmo.lights.Light` for the corresponding cube.
        """
        index = self._get_index(cube_id)
        return self._cube_lights[index]

    def get_cube_id(self, note: Note) -> int:
        """Get the Cube ID for a corresponding note.

        :param note: The :class:`~song_match.song.note.Note` of the song.
        :return: :attr:`~cozmo.objects.LightCube.cube_id`
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
