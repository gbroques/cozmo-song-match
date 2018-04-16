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

#: :class:`~cozmo.lights.Light` - Blue light instance.
BLUE_LIGHT = __get_light(0, 0, 255)

#: :class:`~cozmo.lights.Light` - Purple light instance.
PURPLE_LIGHT = __get_light(150, 0, 255)

#: :class:`~cozmo.lights.Light` - Green light instance.
GREEN_LIGHT = __get_light(0, 255, 0)

#: :class:`~cozmo.lights.Light` - Turquoise light instance.
TURQUOISE_LIGHT = __get_light(0, 255, 190)

#: :class:`~cozmo.lights.Light` - Salmon pink light instance.
SALMON_PINK_LIGHT = __get_light(255, 153, 153)

#: :class:`~cozmo.lights.Light` - Dark red light instance.
DARK_RED_LIGHT = __get_light(153, 0, 0)

#: :class:`~cozmo.lights.Light` - Hot pink light instance.
HOT_PINK_LIGHT = __get_light(255, 102, 204)

#: :class:`~cozmo.lights.Light` - Aquamarine light instance.
AQUAMARINE_LIGHT = __get_light(51, 204, 204)

#: :class:`~cozmo.lights.Light` - Pale yellow light instance.
PALE_YELLOW_LIGHT = __get_light(255, 255, 153)

#: :class:`~cozmo.lights.Light` - Dark blue light instance.
DARK_BLUE_LIGHT = __get_light(0, 0, 204)

#: :class:`~cozmo.lights.Light` - Deep pink light instance.
DEEP_PINK_LIGHT = __get_light(204, 0, 153) 