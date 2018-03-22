from cozmo.objects import EvtObjectTapped
from cozmo.robot import Robot

from song_match.cube import NoteCube
from song_match.cube import NoteCubes
from .song import MaryHadALittleLamb
from .song import Note


class SongMatch:
    """A game where Cozmo plays notes of a song, and the player has to match the notes by tapping blocks."""

    def __init__(self):
        self._robot = None
        self._song = MaryHadALittleLamb()
        Note.init_mixer()

    async def play(self, robot: Robot) -> None:
        """Play the Song Match game.
        Pass this function into cozmo.run_program.
        :param robot: Cozmo Robot instance.
        :return: None
        """
        self._robot = robot
        self._setup()
        await self._init_game_loop()

    def _setup(self) -> None:
        self._robot.world.add_event_handler(EvtObjectTapped, self._tap_handler)
        self._turn_on_cube_lights()

    async def _tap_handler(self, evt, obj=None, tap_count=None, **kwargs):
        cube = evt.obj
        note_cube = NoteCube(cube, self._song)
        await note_cube.blink_and_play_note()

    def _turn_on_cube_lights(self) -> None:
        note_cubes = NoteCubes(self._get_cubes(), self._song)
        note_cubes.turn_on_lights()

    def _get_cubes(self):
        """Convenience method to get the light cubes."""
        return self._robot.world.light_cubes.values()

    async def _init_game_loop(self) -> None:
        while True:
            await self._robot.world.wait_for(EvtObjectTapped)
