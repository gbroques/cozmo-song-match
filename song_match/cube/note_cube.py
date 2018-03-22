from asyncio import sleep

from song_match.song import Song


class NoteCube:
    """Wrapper class for a cube to play a note when tapped."""

    _BLINK_TIME = 0.1  # Controls how long the cube blinks for in seconds

    def __init__(self, cube, song: Song):
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
        cube_light = self._song.get_cube_light(self._cube.cube_id)
        self._cube.set_lights(cube_light)
