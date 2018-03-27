"""Module containing :class:`~song_match.song_match.SongMatch`."""

from cozmo.objects import EvtObjectTapped
from cozmo.robot import Robot

from song_match.cube import NoteCube
from song_match.cube import NoteCubes
from .song import MaryHadALittleLamb
from .song import Note
from .song_robot import SongRobot


class SongMatch:
    """Main game class."""

    def __init__(self):
        self._robot = None
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

        notes = [Note('E4'), Note('D4'), Note('C4')]
        await self._robot.play_notes(notes)

    async def __tap_handler(self, evt, obj=None, tap_count=None, **kwargs):
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
        while True:
            await self._robot.world.wait_for(EvtObjectTapped)
