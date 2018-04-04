"""Module containing :class:`~song_match.cube.note_cube.NoteCube`."""

from asyncio import sleep

from cozmo.lights import Light
from cozmo.objects import LightCube

from song_match.song import Note
from song_match.song import Song


class NoteCube:
    """Wrapper class for a :class:`~cozmo.objects.LightCube` to play a note when tapped."""

    _BLINK_TIME = 0.1  # Controls how long the cube blinks for in seconds

    def __init__(self, cube: LightCube, song: Song):
        self._cube = cube
        self._song = song

    async def blink_and_play_note(self) -> None:
        """Blink the cube and play the corresponding note.

        :return: None
        """
        sleep_duration = self._BLINK_TIME / 2
        self._cube.set_lights_off()
        await sleep(sleep_duration)
        self._song.play_note(self._cube.cube_id)
        await sleep(sleep_duration)
        self.turn_on_light()

    def turn_on_light(self) -> None:
        """Turn on the light for the cube assigned in :class:`~song_match.song.song.Song`.
        
        :return: None
        """
        cube_light = self._song.get_cube_light(self._cube.cube_id)
        self.set_lights(cube_light)

    def set_lights_off(self) -> None:
        """Wrapper method for :meth:`~cozmo.objects.LightCube.set_lights_off`.

        :return: None
        """
        self._cube.set_lights_off()

    def set_lights(self, light: Light) -> None:
        """Wrapper method for :meth:`~cozmo.objects.LightCube.set_lights`.

        :return: None
        """
        self._cube.set_lights(light)

    async def flash(self, light: Light, num_times: int, delay=0.15) -> None:
        """Flash a light a certain number of times.

        :param light: The light to flash.
        :param num_times: The number of times to flash the light.
        :param delay: Time in seconds between turning the light on and off.
                      Default is 0.15 seconds.
        :return: None
        """
        for _ in range(num_times):
            self.set_lights_off()
            await sleep(delay)
            self.set_lights(light)
            await sleep(delay)

    @property
    def note(self) -> Note:
        """Property to access the :class:`~song_match.song.note.Note` of a cube.

        :return: :class:`~song_match.song.note.Note`
        """
        return self._song.get_note(self._cube.cube_id)

    @property
    def cube_id(self) -> int:
        """Property to access the :attr:`~cozmo.objects.LightCube.cube_id` of a cube.

        :return: :attr:`~cozmo.objects.LightCube.cube_id`
        """
        return self._cube.cube_id
