from printerface import *

import time


from ev3dev2.led import Leds
from ev3dev2.motor import (
    LargeMotor,
    MediumMotor,
    OUTPUT_A,
    OUTPUT_B,
    OUTPUT_C,
    SpeedDPS,
)
from ev3dev2.button import Button
from ev3dev2.display import Display
import ev3dev2.fonts as fonts


class Brick(IHub):
    def __init__(self):
        self.titlefont = fonts.load("lutBS18")
        self.leds = Leds()
        self.buttons = Button()
        self.display = Display()

    def busy(self):
        self.leds.set_color("LEFT", "AMBER")
        self.leds.set_color("RIGHT", "AMBER")

    def waiting(self):
        self.leds.set_color("LEFT", "RED")
        self.leds.set_color("RIGHT", "RED")

    def wait_no_presses(self):
        self.buttons.wait_for_released(
            [Button.enter, Button.left, Button.right, Button.up, Button.down]
        )

    def choice(self):
        while True:
            if self.hub.buttons.enter:
                return False
            elif self.hub.buttons.up or self.hub.buttons.down:
                return True
            time.sleep(0.01)

    def title(self, text):
        self.text(text, 0, 50, clear_screen=True)

    def text(self, text, x=0, y=0, clear_screen=False):
        if clear_screen:
            self.display.clear()
        self.display.draw.text((x, y), text)
        self.display.update()


class Pen:
    SPEED = 200
    PRESS_SPEED = SPEED
    PRESS_ANGLE = 90
    ASPECT = 90 / 114  # W/H
    PIXELSIZE = 35

    def __init__(self):
        self.brick = Brick()
        self.x = LargeMotor(OUTPUT_A)
        self.y = LargeMotor(OUTPUT_B)
        self.z = MediumMotor(OUTPUT_C)

    def up(self):
        self.z.on_for_degrees(SpeedDPS(Pen.PRESS_SPEED), -Pen.PRESS_ANGLE)

    def down(self):
        self.z.on_for_degrees(SpeedDPS(Pen.PRESS_SPEED), Pen.PRESS_ANGLE)

    def initialize(self):
        self.brick.title("Calibration\nX and Y")
        self.brick.waiting()
        # x and y manual calibration
        while not self.brick.buttons.enter:
            if self.brick.buttons.left:
                self.x.on(SpeedDPS(-Pen.SPEED))
            elif self.brick.buttons.right:
                self.x.on(SpeedDPS(Pen.SPEED))
            else:
                self.x.off()

            if self.brick.buttons.up:
                self.y.on(SpeedDPS(Pen.SPEED))
            elif self.brick.buttons.down:
                self.y.on(SpeedDPS(-Pen.SPEED))
            else:
                self.y.off()

            time.sleep(0.01)

        self.brick.wait_no_presses()
        self.brick.title("Calibration\nZ (Pen)")

        # z manual calibration
        broken_press = False
        while not self.brick.buttons.enter:
            if self.brick.buttons.up:
                self.z.on(SpeedDPS(-60))
                broken_press = True
            elif self.brick.buttons.down:
                self.z.on(SpeedDPS(60))
                broken_press = True
            else:
                self.z.off()

            time.sleep(0.01)

        if broken_press:
            self.up()

        self.x.reset()
        self.y.reset()
        self.z.reset()

    def dotcoord(self, x, y):
        self.x.on_to_position(SpeedDPS(Pen.SPEED), -x)
        self.y.on_to_position(SpeedDPS(Pen.SPEED), -y * Pen.ASPECT)
        self.down()
        self.up()

    def gohome(self):
        self.x.on_to_position(SpeedDPS(Pen.SPEED), 0, block=False)
        # TODO block=False and check later for both
        self.y.on_to_position(SpeedDPS(Pen.SPEED), 0)
