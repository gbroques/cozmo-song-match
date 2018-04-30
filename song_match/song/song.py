"""Module containing :class:`~song_match.song.song.Song`."""

from abc import ABC, abstractmethod
from typing import List

from cozmo.lights import Light

from song_match.song.note import Note


class Song(ABC):
    """Abstract base class for songs.

    Currently only supports songs with 3 notes.

    Must override **4** abstract properties:

    1. ``_notes`` - A list of 3 :class:`~song_match.song.note.Note` instances in ascending order by pitch.
    2. ``_sequence`` - A sequence of :class:`~song_match.song.note.Note` instances that make up the song.
    3. ``_cube_lights`` - A list of 3 :class:`~cozmo.lights.Light` instances.
    4. ``_difficulty_markers`` - A list of indices where the song ramps up in difficulty.
    """

    def get_note(self, cube_id: int) -> Note:
        """Get the :class:`~song_match.song.note.Note` for a corresponding cube.

        :param cube_id: :attr:`~cozmo.objects.LightCube.cube_id`
        :return: The :class:`~song_match.song.note.Note` of the cube.
        """
        index = self._get_index(cube_id)
        return self._notes[index]

    def play_note(self, cube_id: int) -> None:
        """Play the note for a corresponding cube.

        :param cube_id: :attr:`~cozmo.objects.LightCube.cube_id`
        :return: None
        """
        note = self.get_note(cube_id)
        return note.play()

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

    def get_sequence(self) -> List[Note]:
        """Get the sequence of notes.

        :return: A sequence of notes.
        """
        return self._sequence

    def get_sequence_slice(self, end: int) -> List[Note]:
        """Get a slice of the sequence up to and including end.

        :param end: The end position of the sequence.
        :return: A sequence of notes up until a certain position.
        """
        return self._sequence[0:end]

    def is_not_finished(self, position: int) -> bool:
        """Returns whether or not the song is finished based upon the position in the sequence.

        :param position: The position in the sequence of notes.
        :return: True if the song is not finished. False otherwise.
        """
        return not self.is_finished(position)

    def is_finished(self, position: int) -> bool:
        """Returns whether or not the song is finished based upon the position in the sequence.

        :param position: The position in the sequence of notes.
        :return: True if the song is finished. False otherwise.
        """
        return position > self.length

    def get_difficulty_markers(self) -> List[int]:
        """Markers which determine at what position the song ramps up in difficulty.

        There are two difficulty markers:
        1. Medium
        2. and Long

        The game starts incrementing by 1 note at a time.
        Once the game reaches medium, it increments by 2 notes at a time.
        Once the game reaches long, it increments by 3 notes at a time.

        :return: A list of difficulty markers.
        """
        return self._difficulty_markers

    def get_medium_difficulty_marker(self) -> int:
        """Get the medium difficulty length marker.

        :return: Medium difficulty marker.
        """
        medium, long = self._difficulty_markers
        return medium

    def is_sequence_long(self, sequence_length: int) -> bool:
        """Get whether the length of a sequence is long.

        "Long" is defined as being greater than the medium difficulty marker.

        :param sequence_length: The length of a sequence of notes.
        :return: Whether the sequence is long
        """
        medium_difficulty_marker = self.get_medium_difficulty_marker()
        return sequence_length > medium_difficulty_marker

    @property
    def length(self) -> int:
        """Property for accessing the length of the song.

        :return: The length of the song.
        """
        return len(self._sequence)

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

    @property
    @abstractmethod
    def _difficulty_markers(self) -> List[int]:
        """A list of indices where the song ramps up in difficulty."""
