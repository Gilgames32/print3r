#!/usr/bin/env python3

from time import sleep
from json import load
from csv import reader

from ev3dev2.led import Leds
from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedDPS
from ev3dev2.button import Button
from ev3dev2.display import Display
import ev3dev2.fonts as fonts

TitleFont = fonts.load("lutBS18")

class Brick:
    def __init__(self):
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
        self.buttons.wait_for_released([Button.enter, Button.left, Button.right, Button.up, Button.down])

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
    ASPECT = 1 # W/H TODO: calibrate
    PIXELSIZE = 25

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
            
            sleep(0.01)

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

            sleep(0.01)

        if broken_press:
            self.up()
        
        self.x.reset()
        self.y.reset()
        self.z.reset()
    
    def dot(self, x, y):
        self.x.on_to_position(SpeedDPS(Pen.SPEED), -x * Pen.ASPECT)
        self.y.on_to_position(SpeedDPS(Pen.SPEED), -y)
        self.down()
        self.up()

    def gohome(self):
        self.x.on_to_position(SpeedDPS(Pen.SPEED), 0, block=False)
        self.y.on_to_position(SpeedDPS(Pen.SPEED), 0) # TODO block=False and check later for both

    def image(self):
        with open("palette.json", "r") as palettefile:
            palette = load(palettefile)

        img = []
        with open("image.csv", "r") as csvfile:
            csvreader = reader(csvfile)
            for row in csvreader:
                img.append([int(pixel) for pixel in row])

        # too much voodoo or divine intellect? call it
        flat_img = [pixel for row in img for pixel in row]

        for key, color in palette.items():
            i = int(key)
            if i == 0:
                continue
            
            color["count"] = flat_img.count(i)
            if color["count"] == 0:
                continue

            self.brick.text("Color\n" + color["name"] + "\nDots\n" + str(color["count"]), x=0, y=0, clear_screen=True)
            self.brick.wait_no_presses()

            self.brick.waiting()
            skipcolor = False
            while True:
                if self.brick.buttons.enter:
                    break
                elif self.brick.buttons.up or self.brick.buttons.down:
                    skipcolor = True
                    break
                sleep(0.01)

            if skipcolor:
                continue

            self.brick.busy()

            self.dot(i * Pen.PIXELSIZE, -2 * Pen.PIXELSIZE)

            for y, row in enumerate(img):
                if y % 2 == 0:
                    for x, pixel in enumerate(row):
                        if pixel == i:
                            self.dot(x * Pen.PIXELSIZE, y * Pen.PIXELSIZE)
                else:
                    for x, pixel in reversed(list(enumerate(row))):
                        if pixel == i:
                            self.dot(x * Pen.PIXELSIZE, y * Pen.PIXELSIZE)


pen = Pen()
pen.initialize()
pen.image()
pen.gohome()

sleep(5)

