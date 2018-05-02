from asyncio import sleep
from typing import List

from cozmo.objects import EvtObjectTapped
from cozmo.objects import LightCubeIDs

from .cube import NoteCubes
from .song_robot import SongRobot
from .sound_effects import play_collect_point_sound


class OptionPrompter:
    """A class to help the user select an option from three different choices."""

    def __init__(self, song_robot: SongRobot):
        self._song_robot = song_robot

    async def get_option(self, prompt: str, options: List[str]) -> int:
        """Prompts the user to select from three different options by tapping a cube.

        1. Cozmo will prompt the user with ``prompt``.
        2. Cozmo will point to each cube saying the corresponding ``option``.
        3. The light chaser effect will start signaling the game is awaiting user input.
        4. Upon successful tap ``collect-point.wav`` is played and the cube flashes green.

        :param prompt: The prompt for Cozmo to say.
        :param options: A list of options associated with each cube.
        :return: :attr:`~cozmo.objects.LightCube.cube_id` of the tapped cube.
        """
        assert len(options) == 3

        await self._song_robot.say_text(prompt).wait_for_completed()
        sleep(1)
        for i, cube_id in enumerate(LightCubeIDs):
            prompt = options[i]
            await self._song_robot.say_text(prompt).wait_for_completed()
            action = await self._song_robot.tap_cube(cube_id)
            await action.wait_for_completed()

        note_cubes = NoteCubes.of(self._song_robot)
        note_cubes.start_light_chasers()

        event = await self._song_robot.world.wait_for(EvtObjectTapped)
        cube_id = event.obj.cube_id
        note_cubes.stop_light_chasers()
        play_collect_point_sound()
        await note_cubes.flash_single_cube_green(cube_id)
        await sleep(1)
        return cube_id
