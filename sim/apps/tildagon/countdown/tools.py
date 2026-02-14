from ..common.gamma import gamma_corrections


def decimalise_colour(rgb):
    """Scale a colour to 0-1."""
    return [c / 255 for c in rgb]


def get_interval(interval, unit):
    """Work out the interval string."""
    if "divisor" in unit:
        interval = interval / unit["divisor"]

    if "rounding" in unit:
        interval = round(interval, unit["rounding"])
    else:
        interval = int(interval)

    return interval


def led_correct(colour):
    """Correct an LED colour."""
    brightness = 0.5
    return [gamma_corrections[int(c * brightness)] for c in colour]


def assign_angles(length, angle):
    """Assign spread of angles."""
    start_angle = angle * ((length - 1) / 2)

    return [start_angle - (i * angle) for i in range(length)]


def assign_offsets(length, scale):
    """Assign offsets."""
    raw = [scale * i * 8 for i in range(length)]
    return [x - (scale * 8 * ((length - 1) / 2)) for x in raw]
