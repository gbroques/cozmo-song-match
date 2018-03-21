import asyncio

import cozmo
from pygame.mixer import init

from .note import Note


class SongMatch:
    BLINK_TIME = 0.1  # Controls how long the cube blinks for in seconds

    def __init__(self):
        self.robot = None
        init(frequency=44100, size=-16, channels=1, buffer=1024)

    async def play(self, robot: cozmo.robot.Robot):
        self.robot = robot
        await self._setup()
        await self._init_game_loop()

    async def _setup(self):
        self._C4 = Note('C4')
        self._D4 = Note('D4')
        self._E4 = Note('E4')
        self.robot.world.add_event_handler(cozmo.objects.EvtObjectTapped, self._tap_handler)
        await self._set_cube_lights()

    async def _init_game_loop(self):
        while True:
            await self.robot.world.wait_for(cozmo.objects.EvtObjectTapped)

    async def _tap_handler(self, evt, obj=None, tap_count=None, **kwargs):
        cube = evt.obj
        await self._blink_cube_and_play_note(cube, self.BLINK_TIME)

    async def _blink_cube_and_play_note(self, cube, time):
        cube.set_lights(cozmo.lights.off_light)
        await asyncio.sleep(time / 2)
        self._play_note(cube)
        await asyncio.sleep(time / 2)
        await self._set_cube_light(cube)

    def _play_note(self, cube):
        if cube.object_id == 1:
            self._C4.play()
        elif cube.object_id == 2:
            self._D4.play()
        elif cube.object_id == 3:
            self._E4.play()

    async def _set_cube_lights(self):
        cubes = self.robot.world.light_cubes.values()
        for cube in cubes:
            await self._set_cube_light(cube)

    async def _set_cube_light(self, cube):
        if cube.object_id == 1:
            cube.set_lights(self._get_light(255, 0, 0))
        elif cube.object_id == 2:
            cube.set_lights(self._get_light(255, 172, 0))
        elif cube.object_id == 3:
            cube.set_lights(self._get_light(255, 241, 0))

    @staticmethod
    def _get_light(red, green, blue):
        return cozmo.lights.Light(on_color=cozmo.lights.Color(rgb=(red, green, blue)))
