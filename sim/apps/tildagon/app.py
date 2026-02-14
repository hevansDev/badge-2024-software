import time
from math import atan2

import imu
import ntptime
from events.input import BUTTON_TYPES, Buttons
from system.eventbus import eventbus
from system.patterndisplay.events import PatternDisable
from tildagonos import tildagonos

import app

from .base.conf import conf
from .base.background import Background
from .countdown.tools import decimalise_colour, get_interval, led_correct
from .countdown.word import Word


class Countdown(app.App):
    """Countdown."""

    def __init__(self):
        """Construct."""
        eventbus.emit(PatternDisable())
        ntptime.settime()

        self.button_states = Buttons(self)
        self.conf = conf

        self.year = str(conf["year"])
        self.pallette = self.conf["colours"]["pallettes"][self.year]
        self.screen_colours = self.conf["colours"]["screen"][self.year]

        self.units = self.conf["units"]
        self.unit_index = 3

        self.rotation_offset = 0

        self.resolve_colours()

    def update(self, _):
        """Update."""
        self.scan_buttons()

        acc = imu.acc_read()
        weighting = min(1.0, int(abs(10 - acc[2])) / 9)
        self.rotation_offset = (atan2(acc[1], acc[0])) * weighting

        now = time.time()

        self.interval = self.conf["emf-seconds"] - now
        self.unit = self.units[self.unit_index]

        self.light_leds()

    def draw(self, ctx):
        """Draw."""
        self.overlays = []
        self.overlays.append(
            Background(colour=self.display_colours["background"], opacity=0.85)
        )

        ctx.rotate(-self.rotation_offset)
        self.write_text()

        self.draw_overlays(ctx)

    def write_text(self):
        """Write the text."""
        our_interval = get_interval(self.interval, self.unit)

        verb = "are"
        unit_name = self.unit["name"]

        if our_interval == 1:
            verb = "is"
            unit_name = unit_name[:-1]

        interval_size = "large"
        if len(str(our_interval)) > 6:
            interval_size = "medium"

        strings = (
            (f"There {verb}", "small", -65),
            (str(our_interval), interval_size, -37),
            (unit_name, "medium", -5),
            ("until", "small", 20),
            ("EMF", "xlarge", 55),
        )

        for item in strings:
            word = Word(
                {
                    "text": item[0],
                    "scale": self.conf["text"]["sizes"][item[1]],
                    "colour": self.display_colours["text"],
                    "offset": item[2],
                    "letter-opacity": 0.9,
                }
            )
            word.letters(self)

    def scan_buttons(self):
        """Buttons."""
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            self.button_states.clear()
            self.minimise()

        if self.button_states.get(BUTTON_TYPES["UP"]):
            self.button_states.clear()
            if self.unit_index < len(self.units) - 1:
                self.unit_index += 1

        if self.button_states.get(BUTTON_TYPES["DOWN"]):
            self.button_states.clear()
            if self.unit_index > 0:
                self.unit_index -= 1

    def resolve_colours(self):
        """Sort out the colours."""
        self.led_colours = {}

        for name, key in self.conf["colours"]["leds"][self.year].items():
            self.led_colours[name] = led_correct(self.pallette[key])

        self.display_colours = {}
        for name, key in self.conf["colours"]["screen"][self.year].items():
            self.display_colours[name] = decimalise_colour(self.pallette[key])

    def light_leds(self):
        """Light lights."""
        for index in range(18):
            tildagonos.leds[index + 1] = self.led_colours["background"]

        tildagonos.leds[int(12 - (self.interval % 12))] = self.led_colours["ticker"]

        tildagonos.leds.write()


__app_export__ = Countdown
