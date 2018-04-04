"""Module containing :class:`~song_match.cube.note_cubes.NoteCubes`."""

from typing import List

from cozmo.lights import off_light, red_light, Light
from cozmo.objects import LightCube

from song_match.song import Song
from .note_cube import NoteCube

FLASH_DELAY = 0.15


class NoteCubes:
    """Container class for three :class:`~cozmo.objects.LightCube` instances."""

    def __init__(self, cubes: List[LightCube], song: Song):
        self._cubes = cubes
        self._song = song

    def turn_on_lights(self) -> None:
        """Turn on the light for each note cube.

        This method turns on the lights assigned in
        :class:`~song_match.song.song.Song`.

        :return: None
        """
        for cube in self._cubes:
            note_cube = NoteCube(cube, self._song)
            note_cube.turn_on_light()

    async def flash_light_red(self, cube_id: int) -> None:
        """Convenience method for calling :meth:`~song_match.cube.note_cubes.NoteCubes.flash_light`
        with a :data:`~cozmo.lights.red_light`.

        :param cube_id: :attr:`~cozmo.objects.LightCube.cube_id`
        :return: None
        """
        await self.flash_light(cube_id, red_light)

    async def flash_light(self, cube_id: int, light: Light) -> None:
        """Flashes the light of a particular cube,
        while turning off the lights of the other cubes.

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
