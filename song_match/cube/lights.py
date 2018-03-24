from cozmo.lights import Color, Light


def __get_light(red: int, green: int, blue: int) -> Light:
    color = Color(rgb=(red, green, blue))
    return Light(on_color=color)


RED_LIGHT = __get_light(255, 0, 0)
ORANGE_LIGHT = __get_light(255, 172, 0)
YELLOW_LIGHT = __get_light(255, 241, 0)
