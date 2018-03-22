from cozmo.lights import Color, Light


def _get_light(red: int, green: int, blue: int) -> Light:
    color = Color(rgb=(red, green, blue))
    return Light(on_color=color)


RED_LIGHT = _get_light(255, 0, 0)
ORANGE_LIGHT = _get_light(255, 172, 0)
YELLOW_LIGHT = _get_light(255, 241, 0)
