from typing import Dict
from typing import List

from cozmo.objects import LightCubeIDs, LightCube


class CubeMat:
    """Class to convert cube IDs to mat positions and vise versa.

    Each cube has an ID of 1, 2, or 3 associated with it.

    Consider the following cubes with IDs from left to right::

         _______      _______     _______
        |       |    |       |   |       |
        |   2   |    |   1   |   |   3   |
        |_______|    |_______|   |_______|

    The mat position of each cube from the player's perspective is as follows::

         _______      _______     _______
        |       |    |       |   |       |
        |   1   |    |   2   |   |   3   |
        |_______|    |_______|   |_______|

    Where the the left-most position is assigned 1,
    middle position 2, and right-most position 3.

    This class is responsible for converting from one to the other.

    In this example, the conversion from *cube id* to *mat position* is:

    * 2 -> 1
    * 1 -> 2
    * 3 -> 3
    """
    __cube_order = None  # type: Dict[int, int]

    @classmethod
    def get_positions(cls) -> List[int]:
        """Get a list of mat positions ordered by cube ID.

        :return: A list of mat positions ordered by cube ID.
        """
        return list(cls.__cube_order.values())

    @classmethod
    def order_cubes_by_position(cls, song_robot) -> None:
        """Assign each cube ID to a mat position.

        :param song_robot: :class:`~song_match.song_robot.SongRobot`
        :return: None
        """
        cubes = cls.get_light_cubes(song_robot)
        sorted_cubes = sorted(cubes, key=lambda cube: cube.pose.position.y)
        sorted_cube_ids = list(map(lambda cube: cube.cube_id, sorted_cubes))
        cls.__cube_order = dict(zip(LightCubeIDs, sorted_cube_ids))

    @classmethod
    def get_light_cubes(cls, song_robot) -> List[LightCube]:
        """Convenience method to get a list of light cubes.

        Note:
            This is duplicated in song_match.cube.util due to import issues.

        :param song_robot: :class:`~song_match.song_robot.SongRobot`
        :return: A list of three :class:`~cozmo.objects.LightCube` instances.
        """
        return list(song_robot.robot.world.light_cubes.values())

    @classmethod
    def position_to_cube_id(cls, cube_id: int) -> int:
        """Maps a mat position to a :attr:`~cozmo.objects.LightCube.cube_id`.

        :param cube_id: The ordered cube ID.
        :return: :attr:`~cozmo.objects.LightCube.cube_id`
        """
        cube_ids = list(cls.__cube_order.keys())
        order = list(cls.__cube_order.values())
        return cube_ids[order.index(cube_id)]

    @classmethod
    def cube_id_to_position(cls, cube_id: int) -> int:
        """Maps the :attr:`~cozmo.objects.LightCube.cube_id` to a mat position.

        :param cube_id: :attr:`~cozmo.objects.LightCube.cube_id`
        :return: The ordered cube ID.
        """
        return cls.__cube_order[cube_id]
