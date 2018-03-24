from asyncio import sleep
from typing import List

from cozmo.anim import EvtAnimationCompleted
from cozmo.anim import Triggers
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id
from cozmo.robot import Robot
from cozmo.util import radians

from .cube import NoteCube
from .song import Song, Note


class SongRobot:
    """Wrapper class for Cozmo Robot instance."""

    _NOTE_DELAY = 0.2  # Time to delay blinking the cube and playing the note
    _SLEEP_TIME = 0.1  # Time to sleep for while animation finishes

    def __init__(self, robot: Robot, song: Song):
        self._robot = robot
        self._song = song
        self._prev_cube_id = LightCube2Id  # Keep track of previously tapped cube
        self._animation_complete = True  # Keep track of when animation is completed
        self._robot.world.add_event_handler(EvtAnimationCompleted, self.__on_animation_completed)

    async def play_notes(self, notes: List[Note]) -> None:
        for note in notes:
            await self.play_note(note)

    async def play_note(self, note: Note) -> None:
        cube_id = self._song.get_cube_id(note)
        note_cube = self.__get_note_cube(cube_id)
        self.__tap_cube(cube_id)
        await sleep(self._NOTE_DELAY)
        await note_cube.blink_and_play_note()
        await self.__wait_until_animation_finished()

    def __get_note_cube(self, cube_id):
        cube = self._robot.world.get_light_cube(cube_id)
        return NoteCube(cube, self._song)

    def __tap_cube(self, cube_id) -> None:
        animation = self.__get_tap_animation(cube_id)
        self.__play_animation(animation)
        self._prev_cube_id = cube_id

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

    def __play_animation(self, animation_trigger: Triggers):
        self._animation_complete = False
        self._robot.play_anim_trigger(animation_trigger, in_parallel=True)

    async def __wait_until_animation_finished(self):
        while not self._animation_complete:
            await sleep(self._SLEEP_TIME)

    def __on_animation_completed(self, evt, animation_name, **kwargs):
        self._animation_complete = True

    async def __turn_back_to_center(self):
        turn_to = radians(-self._robot.pose_angle.radians)
        await self._robot.turn_in_place(turn_to).wait_for_completed()

    @property
    def world(self):
        return self._robot.world
