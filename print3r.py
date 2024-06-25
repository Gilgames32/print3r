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

# ev3 brick implementation of the ihub interface
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
            if self.buttons.enter:
                return True
            elif self.buttons.up or self.buttons.down:
                return False
            time.sleep(0.01)

    def title(self, text):
        self.text(text, 0, 50, clear_screen=True)

    def text(self, text, x=0, y=0, clear_screen=False):
        if clear_screen:
            self.display.clear()
        self.display.draw.text((x, y), text)
        self.display.update()


# lego implementation of the ipen interface
class Pen(IPen):
    SPEED = 360
    SLOW_SPEED = 60
    PRESS_SPEED = SPEED
    PRESS_ANGLE = 90
    ASPECT = 90 / 114  # W/H
    PIXELSIZE = 35

    def __init__(self):
        self.brick = Brick()
        self.x = LargeMotor(OUTPUT_A)
        self.y = LargeMotor(OUTPUT_B)
        self.z = MediumMotor(OUTPUT_C)
        self.headpos = (0, 0)
        self.headup = False
        # TODO polarity

    def up(self):
        if self.headup:
            return
        self.z.on_for_degrees(SpeedDPS(Pen.PRESS_SPEED), -Pen.PRESS_ANGLE)
        self.headup = True

    def down(self):
        if not self.headup:
            return
        self.z.on_for_degrees(SpeedDPS(Pen.PRESS_SPEED), Pen.PRESS_ANGLE)
        self.headup = False

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
                self.z.on(SpeedDPS(-Pen.SLOW_SPEED))
                broken_press = True
            elif self.brick.buttons.down:
                self.z.on(SpeedDPS(Pen.SLOW_SPEED))
                broken_press = True
            else:
                self.z.off()

            time.sleep(0.01)

        if broken_press:
            self.up()

        self.headup = True
        self.resetpos()

    def resetpos(self):
        self.headpos = (0, 0)
        self.x.reset()
        self.y.reset()
        self.z.reset()

    def dotcoord(self, x, y):
        x *= Pen.PIXELSIZE
        y *= Pen.PIXELSIZE
        self.x.on_to_position(SpeedDPS(Pen.SPEED), -x)
        self.y.on_to_position(SpeedDPS(Pen.SPEED), -y * Pen.ASPECT)
        self.down()
        self.up()

    def goto(self, x, y):
        dx = x - self.headpos[0]
        dy = y - self.headpos[1]

        if dx == 0 and dy == 0:
            return

        if dx == 0:  # vertical line
            speed_x = 0
            speed_y = Pen.SPEED
        elif dy == 0:  # horizontal line
            speed_x = Pen.SPEED
            speed_y = 0
        else:
            slope = dy / dx
            speed_x = Pen.SPEED / (1 + slope**2) ** 0.5
            speed_y = speed_x * slope

        self.x.on_to_position(SpeedDPS(speed_x), -x, block=False)
        self.y.on_to_position(
            SpeedDPS(speed_y * Pen.ASPECT), -y * Pen.ASPECT, block=False
        )
        self.x.wait_until_not_moving()
        self.y.wait_until_not_moving()
        self.headpos = (x, y)

    def line(self, x1, y1, x2, y2):
        if self.headpos != (x1, y1):
            self.up()
            self.goto(x1, y1)
        self.down()
        self.goto(x2, y2)

    def gohome(self):
        self.x.on_to_position(SpeedDPS(Pen.SPEED), 0, block=False)
        self.y.on_to_position(SpeedDPS(Pen.SPEED * Pen.ASPECT), 0, block=False)
        self.x.wait_until_not_moving()
        self.y.wait_until_not_moving()
        self.headpos = (0, 0)

    def empty(self):
        self.up()
        self.gohome()
        self.y.on_for_rotations(SpeedDPS(720), -12)

    def adjust(self):
        broken = False
        self.gohome()

        self.brick.title("Adjust\nX and Y")
        self.brick.waiting()
        # x and y manual calibration
        while not self.brick.buttons.enter:
            if self.brick.buttons.left:
                self.x.on(SpeedDPS(-Pen.SLOW_SPEED))
                broken = True
            elif self.brick.buttons.right:
                self.x.on(SpeedDPS(Pen.SLOW_SPEED))
                broken = True
            else:
                self.x.off()

            if self.brick.buttons.up:
                self.y.on(SpeedDPS(Pen.SLOW_SPEED))
                broken = True
            elif self.brick.buttons.down:
                self.y.on(SpeedDPS(-Pen.SLOW_SPEED))
                broken = True
            else:
                self.y.off()

            time.sleep(0.01)

        self.brick.wait_no_presses()
        self.brick.title("Adjust\nZ (Pen)")

        # z manual calibration
        while not self.brick.buttons.enter:
            if self.brick.buttons.up:
                self.z.on(SpeedDPS(-Pen.SLOW_SPEED / 2))
                broken = True
            elif self.brick.buttons.down:
                self.z.on(SpeedDPS(Pen.SLOW_SPEED / 2))
                broken = True
            else:
                self.z.off()

            time.sleep(0.01)

        if broken:
            self.resetpos()

        return not broken
