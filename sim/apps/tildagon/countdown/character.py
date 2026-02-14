from math import cos, radians, sin
from random import randint, random

from ..base.conf import conf
from ..countdown.font import font


class Character:
    """A character."""

    def __init__(self, params=None):
        """Construct."""
        params = params if params else {}
        self.char = params.get("char")
        self.scale = params.get("scale")
        self.angle = params.get("angle", 0)
        self.opacity = params.get("opacity", 1)
        self.colour = list(params.get("colour")) + [self.opacity]
        self.offset = params.get("offset")
        self.x_offset = params.get("x-offset", 0)
        self.data = font[self.char]

    def draw(self, ctx):
        """Draw."""
        ctx.rgba(*self.colour)

        ctx.translate(
            sin(radians(self.angle)) * -self.offset,
            cos(radians(self.angle)) * self.offset,
        )
        ctx.rotate(radians(self.angle))

        if self.x_offset:
            ctx.translate(self.x_offset, 0)

        start_x = (
            0
            - (8 * self.scale / 2)
            + (random() < conf["twitch-amount"] and (randint(0, 1) * 2) - 1)
        )
        start_y = (
            0
            - (8 * self.scale / 2)
            + (random() < conf["twitch-amount"] and (randint(0, 1) * 2) - 1)
        )
        for item in self.data:
            left = item[0] * self.scale
            width = item[2] * self.scale
            top = item[1] * self.scale
            height = self.scale

            ctx.rectangle(
                start_x + left,
                start_y + top,
                width,
                height,
            )

            ctx.fill()
