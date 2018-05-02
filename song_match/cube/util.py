from typing import List

from cozmo.objects import LightCube


def get_light_cubes(song_robot) -> List[LightCube]:
    """Convenience method to get a list of light cubes.

    :param song_robot: :class:`~song_match.song_robot.SongRobot`
    :return: A list of three :class:`~cozmo.objects.LightCube` instances.
    """
    return list(song_robot.robot.world.light_cubes.values())


def get_light_cube(song_robot, cube_id: int) -> LightCube:
    """Convenience method to get a light cube instance.

    :param song_robot: :class:`~song_match.song_robot.SongRobot`
    :param cube_id: :attr:`~cozmo.objects.LightCube.cube_id`
    :return: :class:`~cozmo.objects.LightCube`
    """
    return song_robot.world.get_light_cube(cube_id)
