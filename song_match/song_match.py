"""Module containing :class:`~song_match.song_match.SongMatch`."""

from asyncio import sleep
from typing import List

from cozmo.objects import EvtObjectTapped
from cozmo.robot import Robot

from song_match.cube import NoteCube
from song_match.cube import NoteCubes
from .song import MaryHadALittleLamb
from .song import Note
from .song_robot import SongRobot

TIME_IN_BETWEEN_PLAYER_AND_COZMO = 1  # In seconds

STARTING_POSITION = 3  # The number of notes you start with in the sequence

TIME_BETWEEN_NOTES = 0.5


class SongMatch:
    """Main game class."""

    def __init__(self):
        self._robot = None
        self._is_playing_notes = False  # Flag to prevent player from interrupting the game or cozmo playing notes
        self._song = MaryHadALittleLamb()
        Note.init_mixer()

    async def play(self, robot: Robot) -> None:
        """Play the Song Match game.

        Pass this function into :func:`cozmo.run_program`.

        :param robot: Cozmo Robot instance.
        :type robot: :class:`~cozmo.robot.Robot`
        :return: None
        """
        self._robot = SongRobot(robot, self._song)
        await self.__setup()
        await self.__init_game_loop()

    async def __setup(self) -> None:
        await self._robot.world.wait_until_num_objects_visible(3)
        self._robot.world.add_event_handler(EvtObjectTapped, self.__tap_handler)
        self.__turn_on_cube_lights()

    async def __tap_handler(self, evt, obj=None, tap_count=None, **kwargs):
        if self._is_playing_notes:
            return
        cube = evt.obj
        note_cube = NoteCube(cube, self._song)
        await note_cube.blink_and_play_note()

    def __turn_on_cube_lights(self) -> None:
        note_cubes = NoteCubes(self.__get_cubes(), self._song)
        note_cubes.turn_on_lights()

    def __get_cubes(self):
        """Convenience method to get the light cubes."""
        return self._robot.world.light_cubes.values()

    async def __init_game_loop(self) -> None:
        current_position = STARTING_POSITION
        while self._song.is_not_finished(current_position):
            notes = self._song.get_sequence(current_position)
            await self.__play_notes(notes)

            await self.__wait_for_player_to_match_notes(current_position)

            await sleep(TIME_IN_BETWEEN_PLAYER_AND_COZMO)

            await self.__wait_for_cozmo_to_match_notes(notes)

            current_position += 1

    async def __wait_for_cozmo_to_match_notes(self, notes: List[Note]) -> None:
        self._is_playing_notes = True
        await self._robot.play_notes(notes)
        self._is_playing_notes = False

    async def __wait_for_player_to_match_notes(self, current_position: int) -> None:
        num_notes_played = 0
        notes = self._song.get_sequence(current_position)
        while num_notes_played != current_position:
            event = await self._robot.world.wait_for(EvtObjectTapped)
            tapped_cube = NoteCube(event.obj, self._song)
            correct_note = notes[num_notes_played]
            if tapped_cube.note != correct_note:
                exit(0)
            num_notes_played += 1

    async def __play_notes(self, notes: List[Note]) -> None:
        self._is_playing_notes = True
        for note in notes:
            await self.__play_note(note)
            await sleep(TIME_BETWEEN_NOTES)
        self._is_playing_notes = False

    async def __play_note(self, note: Note) -> None:
        cube_id = self._song.get_cube_id(note)
        note_cube = self.__get_note_cube(cube_id)
        await note_cube.blink_and_play_note()

    def __get_note_cube(self, cube_id):
        cube = self._robot.world.get_light_cube(cube_id)
        return NoteCube(cube, self._song)
