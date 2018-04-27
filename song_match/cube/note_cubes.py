"""Module containing :class:`~song_match.cube.note_cubes.NoteCubes`."""

from asyncio import sleep
from typing import List

from cozmo.lights import off_light, green_light, red_light, Light
from cozmo.objects import LightCube

from song_match.song import Song
from song_match.song_robot import SongRobot
from .note_cube import NoteCube


class NoteCubes:
    """Container class for three :class:`~cozmo.objects.LightCube` instances."""

    def __init__(self, cubes: List[LightCube], song: Song):
        self._cubes = cubes
        self._song = song

    @classmethod
    def of(cls, song_robot: SongRobot) -> 'NoteCubes':
        """Static factory method for creating :class:`~song_match.cube.note_cubes.NoteCubes`
        from :class:`~song_match.song_robot.SongRobot`.

        :param song_robot: :class:`~song_match.song_robot.SongRobot`
        """
        cubes = cls.__get_cubes(song_robot)
        return NoteCubes(cubes, song_robot.song)

    @staticmethod
    def __get_cubes(song_robot: SongRobot) -> List[LightCube]:
        return list(song_robot.robot.world.light_cubes.values())

    def turn_on_lights(self) -> None:
        """Turn on the light for each note cube.

        This method turns on the lights assigned in
        :class:`~song_match.song.song.Song`.

        :return: None
        """
        for cube in self._cubes:
            note_cube = NoteCube(cube, self._song)
            note_cube.turn_on_light()

    async def flash_lights_green(self, num_times: int = 3, delay=0.15) -> None:
        """Flash the lights of each cube green.

        :param num_times: The number of times to flash green.
        :param delay: Time in seconds between turning the light on and off.
        :return: None
        """
        for _ in range(num_times):
            self.set_lights_off()
            await sleep(delay)
            self.set_lights(green_light)
            await sleep(delay)
        self.turn_on_lights()

    async def flash_lights(self, num_times: int = 4, delay=0.15) -> None:
        """Flash the lights of each cube.

        :param num_times: The number of times to flash lights.
        :param delay: Time in seconds between turning the light on and off.
        :return: None
        """
        for _ in range(num_times):
            self.set_lights_off()
            await sleep(delay)
            self.turn_on_lights()
            await sleep(delay)

    def set_lights(self, light: Light) -> None:
        """Call :meth:`~cozmo.objects.LightCube.set_lights` for each cube.

        :param light: :class:`~cozmo.lights.Light`
        :return: None
        """
        for cube in self._cubes:
            cube.set_lights(light)

    def set_lights_off(self) -> None:
        """Call :meth:`~cozmo.objects.LightCube.set_lights_off` for each cube.

        :return: None
        """
        for cube in self._cubes:
            cube.set_lights_off()

    async def start_light_chasers(self, time_before_stop=2):
        """Starts the light chaser effect for each cube.

        :param time_before_stop: Time to wait before the light chaser effect stops (in seconds).
        :return: None
        """
        first_cube, second_cube, third_cube = self.__get_note_cubes()
        first_cube.start_light_chaser()
        second_cube.start_light_chaser()
        third_cube.start_light_chaser()
        await sleep(time_before_stop)
        first_cube.stop_light_chaser()
        second_cube.stop_light_chaser()
        third_cube.stop_light_chaser()

    async def end_of_game_lights(self, time_before_switch=1):
        """Starts the end-of-game sequences for the cubes.

        :param time_before_switch: Time to wait before the effect switches between chasers and flashes (in seconds).
        :return: None
        """

        await self.start_light_chasers()
        await self.flash_lights()
        await self.start_light_chasers()
        await self.flash_lights()


    def __get_note_cubes(self) -> List[NoteCube]:
        return list(map(lambda cube: NoteCube(cube, self._song), self._cubes))

    async def flash_single_cube_red(self, cube_id: int) -> None:
        """Convenience method for calling :meth:`~song_match.cube.note_cubes.NoteCubes.flash_single_cube`
        with a :data:`~cozmo.lights.red_light`.

        :param cube_id: :attr:`~cozmo.objects.LightCube.cube_id`
        :return: None
        """
        await self.flash_single_cube(cube_id, red_light)

    async def flash_single_cube(self, cube_id: int, light: Light) -> None:
        """Flashes the light of a single cube,
        while turning the lights of the other cubes off.

        :param cube_id: :attr:`~cozmo.objects.LightCube.cube_id`
        :param light: The :class:`~cozmo.lights.Light` to flash.
        :return: None
        """
        for cube in self._cubes:
            if cube.cube_id == cube_id:
                cube.set_lights(light)
            else:
                cube.set_lights(off_light)
        note_cube = self.__get_note_cube(cube_id)
        await note_cube.flash(light, 3)

        self.turn_on_lights()

    def __get_note_cube(self, cube_id: int) -> NoteCube:
        cube = self.__get_cube(cube_id)
        return NoteCube(cube, self._song)

    def __get_cube(self, cube_id: int) -> LightCube:
        return next(cube for cube in self._cubes if cube.cube_id == cube_id)
