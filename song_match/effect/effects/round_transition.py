from asyncio import sleep

from song_match.effect import Effect
from song_match.sound_effects import play_level_complete_sound


class RoundTransitionEffect(Effect):
    """Played when transitioning between rounds of the game."""

    async def play(self) -> None:
        """Play the round transition effect.

        * Play ``level-complete.wav``.
        * Start the light chaser effect on each cube.

        :return: None
        """
        play_level_complete_sound()
        await self._song_robot.turn_back_to_center(in_parallel=True)
        await self._note_cubes.start_and_stop_light_chasers()
        await sleep(1)
