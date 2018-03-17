import asyncio

import cozmo


class SongMatch:
    BLINK_TIME = 0.2  # Controls how long the cube blinks for in seconds
    CUBE_COLOR = cozmo.lights.blue_light

    def __init__(self):
        self.robot = None

    async def play(self, robot: cozmo.robot.Robot):
        self.robot = robot
        await self._setup()
        await self._init_game_loop()

    async def _setup(self):
        self.robot.world.add_event_handler(cozmo.objects.EvtObjectTapped, self._tap_handler)
        await self._set_cube_lights(self.CUBE_COLOR)

    async def _init_game_loop(self):
        while True:
            await self.robot.world.wait_for(cozmo.objects.EvtObjectTapped)

    async def _tap_handler(self, evt, obj=None, tap_count=None, **kwargs):
        cube = evt.obj
        await self._blink_cube(cube, self.BLINK_TIME)

    async def _blink_cube(self, cube, time):
        cube.set_lights(cozmo.lights.off_light)
        await asyncio.sleep(time)
        cube.set_lights(self.CUBE_COLOR)

    async def _set_cube_lights(self, color):
        cubes = self.robot.world.light_cubes.values()
        for cube in cubes:
            cube.set_lights(color)
