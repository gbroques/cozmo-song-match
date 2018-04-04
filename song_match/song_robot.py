"""Module containing :class:`~song_match.song_robot.SongRobot`."""

from asyncio import sleep
from typing import List

from cozmo.anim import AnimationTrigger
from cozmo.anim import Triggers
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id
from cozmo.robot import Robot, world
from cozmo.util import radians

from .cube import NoteCube
from .song import Song, Note


class SongRobot:
    """Wrapper class for Cozmo :class:`~cozmo.robot.Robot` instance."""

    _NOTE_DELAY = 0.2  # Time to delay blinking the cube and playing the note
    _SLEEP_TIME = 0.1  # Time to sleep for while animation finishes

    def __init__(self, robot: Robot, song: Song):
        self._robot = robot
        self._song = song
        self._prev_cube_id = LightCube2Id  # Keep track of previously tapped cube

    async def play_notes(self, notes: List[Note]) -> None:
        """Make Cozmo play a series of notes.

        :param notes: The series of notes to play.
        :return: None
        """
        for note in notes:
            await self.play_note(note)

    async def play_note(self, note: Note) -> None:
        """Make Cozmo play a note.

        :param note: The :class:`~song_match.song.note.Note` to play.
        :return: None
        """
        cube_id = self._song.get_cube_id(note)
        note_cube = NoteCube.of(self, cube_id)
        action = self.__tap_cube(cube_id)
        await sleep(self._NOTE_DELAY)
        await note_cube.blink_and_play_note()
        await action.wait_for_completed()

    async def turn_back_to_center(self, in_parallel=False) -> None:
        """Turn Cozmo back to the center.

        :param in_parallel: Whether to do the action in parallel or wait until it's completed.
        :return: None
        """
        turn_to = radians(-self._robot.pose_angle.radians)
        if in_parallel:
            self._robot.turn_in_place(turn_to)
        else:
            await self._robot.turn_in_place(turn_to).wait_for_completed()
        self._prev_cube_id = LightCube2Id

    @property
    def world(self) -> world:
        """Property for accessing :attr:`~cozmo.robot.Robot.world`."""
        return self._robot.world

    @property
    def robot(self) -> Robot:
        """Property for accessing :class:`~cozmo.robot.Robot`."""
        return self._robot

    @property
    def song(self) -> Song:
        """Property for accessing :class:`~song_match.song.song.Song`."""
        return self._song

    def __tap_cube(self, cube_id) -> AnimationTrigger:
        animation = self.__get_tap_animation(cube_id)
        action = self.__play_animation(animation)
        self._prev_cube_id = cube_id
        return action

    def __get_tap_animation(self, cube_id) -> Triggers:
        """Returns a tap animation based upon the current and previously tapped cubes."""
        key = (cube_id, self._prev_cube_id)
        return {
            (LightCube1Id, LightCube1Id): Triggers.MemoryMatchPointCenter,
            (LightCube1Id, LightCube2Id): Triggers.MemoryMatchPointRightSmall,
            (LightCube1Id, LightCube3Id): Triggers.MemoryMatchPointRightBig,
            (LightCube2Id, LightCube1Id): Triggers.MemoryMatchPointLeftSmall,
            (LightCube2Id, LightCube2Id): Triggers.MemoryMatchPointCenter,
            (LightCube2Id, LightCube3Id): Triggers.MemoryMatchPointRightSmall,
            (LightCube3Id, LightCube1Id): Triggers.MemoryMatchPointLeftBig,
            (LightCube3Id, LightCube2Id): Triggers.MemoryMatchPointLeftSmall,
            (LightCube3Id, LightCube3Id): Triggers.MemoryMatchPointCenter,
        }[key]

    def __play_animation(self, animation_trigger: Triggers) -> AnimationTrigger:
        return self._robot.play_anim_trigger(animation_trigger, in_parallel=True)
