"""Predefined :class:`~cozmo.lights.Light` instances for Cozmo's cubes."""

from cozmo.lights import Color, Light


def __get_light(red: int, green: int, blue: int) -> Light:
    """Convenience method to get a light from RGB values.

    :param red: Red 0 - 255.
    :param green: Green 0 - 255.
    :param blue: Blue 0 - 255.
    :return: A Light with the corresponding color.
    """
    color = Color(rgb=(red, green, blue))
    return Light(on_color=color)


#: :class:`~cozmo.lights.Light` - Red light instance.
RED_LIGHT = __get_light(255, 0, 0)

#: :class:`~cozmo.lights.Light` - Orange light instance.
ORANGE_LIGHT = __get_light(255, 172, 0)

#: :class:`~cozmo.lights.Light` - Yellow light instance.
YELLOW_LIGHT = __get_light(255, 241, 0)
