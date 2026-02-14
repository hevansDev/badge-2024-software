from .character import Character
from .tools import assign_angles, assign_offsets


class Word:
    """Write letters 'n' shit, yo."""

    def __init__(self, params):
        """Construct."""
        self.text = params.get("text")
        self.scale = params.get("scale")
        self.offset = params.get("offset")
        self.angle = params.get("angle")
        self.colour = params.get("colour")
        self.opacity = params.get("letter-opacity", 1)
        self.offsets = None
        self.angles = None

        if params.get("angle"):
            self.angles = assign_angles(len(self.text), self.angle)
        else:
            self.offsets = assign_offsets(len(self.text), self.scale)

    def letters(self, app):
        """Letters."""
        for index, letter in enumerate(self.text):
            params = {
                "char": letter,
                "scale": self.scale,
                "offset": self.offset,
                "colour": self.colour,
                "opacity": self.opacity,
            }

            if self.angles:
                params["angle"] = self.angles[index]
            if self.offsets:
                params["x-offset"] = self.offsets[index]

            app.overlays.append(Character(params))
