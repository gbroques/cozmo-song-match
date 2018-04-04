"""Module containing :class:`~song_match.song_match.SongMatch`."""

from asyncio import sleep
from sys import exit
from typing import Callable, List

from cozmo.audio import AudioEvents
from cozmo.objects import EvtObjectTapped
from cozmo.objects import LightCube
from cozmo.robot import Robot

from song_match.cube import NoteCube
from song_match.cube import NoteCubes
from .song import MaryHadALittleLamb
from .song import Note
from .song_robot import SongRobot

MAX_STRIKES = 3  # The maximum number of notes a player can get wrong

TIME_IN_BETWEEN_PLAYER_AND_COZMO = 1  # In seconds

STARTING_POSITION = 3  # The number of notes you start with in the sequence

TIME_BETWEEN_NOTES = 0.5


class SongMatch:
    """Main game class."""

    def __init__(self):
        self._robot = None
        self._prevent_tap = False  # Flag to prevent player from interrupting game by tapping cubes
        self._num_player_wrong = 0
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
        if self._prevent_tap:
            return
        cube = evt.obj
        note_cube = NoteCube(cube, self._song)
        await note_cube.blink_and_play_note()

    def __turn_on_cube_lights(self) -> None:
        note_cubes = NoteCubes(self.__get_cubes(), self._song)
        note_cubes.turn_on_lights()

    def __get_cubes(self) -> List[LightCube]:
        return list(self._robot.world.light_cubes.values())

    async def __init_game_loop(self) -> None:
        current_position = STARTING_POSITION
        while self._song.is_not_finished(current_position):
            notes = self._song.get_sequence_slice(current_position)
            await self.__tap_guard(lambda: self.__play_notes(notes))

            await self.__wait_for_player_to_match_notes(current_position)

            await sleep(TIME_IN_BETWEEN_PLAYER_AND_COZMO)

            await self.__tap_guard(lambda: self._robot.play_notes(notes))

            current_position += 1

    async def __wait_for_player_to_match_notes(self, current_position: int) -> bool:
        num_notes_played = 0
        notes = self._song.get_sequence_slice(current_position)
        while num_notes_played != current_position:
            event = await self._robot.world.wait_for(EvtObjectTapped)
            tapped_cube = NoteCube(event.obj, self._song)
            correct_note = notes[num_notes_played]

            if tapped_cube.note != correct_note:
                self._num_player_wrong += 1
                await self.__tap_guard(lambda: self.__play_wrong_note_effect(tapped_cube.cube_id))
                self.__check_for_game_over()
                return False

            num_notes_played += 1
        return True

    def __check_for_game_over(self) -> None:
        if self._num_player_wrong == MAX_STRIKES:
            exit(0)

    async def __tap_guard(self, callable_function: Callable) -> None:
        self._prevent_tap = True
        await callable_function()
        self._prevent_tap = False

    async def __play_wrong_note_effect(self, cube_id: int):
        self._robot.robot.play_audio(AudioEvents.SfxGameLose)
        note_cubes = NoteCubes(self.__get_cubes(), self._song)
        await note_cubes.flash_light_red(cube_id)

    async def __play_notes(self, notes: List[Note]) -> None:
        for note in notes:
            await self.__play_note(note)
            await sleep(TIME_BETWEEN_NOTES)

    async def __play_note(self, note: Note) -> None:
        cube_id = self._song.get_cube_id(note)
        note_cube = self.__get_note_cube(cube_id)
        await note_cube.blink_and_play_note()

    def __get_note_cube(self, cube_id):
        cube = self._robot.world.get_light_cube(cube_id)
        return NoteCube(cube, self._song)
