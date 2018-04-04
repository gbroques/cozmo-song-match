from asyncio import sleep

from song_match.effect import Effect


class RoundTransitionEffect(Effect):

    async def play(self) -> None:
        """Play the round transition effect.

        * Play ``RoundTransitionEffect.wav``.
        * Start the light chaser effect on each cube.

        :return: None
        """
        self._sound.play()
        await self._song_robot.turn_back_to_center(in_parallel=True)
        await self._note_cubes.start_light_chasers()
        await sleep(1)
