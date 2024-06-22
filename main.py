#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port, Color, Button
from pybricks.tools import wait

from csv import reader
from json import load

# brick
ev3 = EV3Brick()
ev3.light.on(Color.RED)


class Pen:
    speed = 512
    press = 90
    aspect = 1.6/2 # w/h, TODO: calibrate
    y_deadangle = -60

    def __init__(self, x_port: Port = Port.A, y_port: Port = Port.B, z_port: Port = Port.C):
        self.x = Motor(x_port)
        self.y = Motor(y_port)
        self.z = Motor(z_port)

    def up(self):
        self.z.run_angle(Pen.speed, -Pen.press)

    def down(self):
        self.z.run_angle(Pen.speed, Pen.press)
    
    def initialize(self):
        # x and y manual calibration
        while Button.CENTER not in ev3.buttons.pressed():
            if Button.LEFT in ev3.buttons.pressed():
                self.x.run(Pen.speed)
            elif Button.RIGHT in ev3.buttons.pressed():
                self.x.run(-Pen.speed)
            else:
                self.x.run(0)

            if Button.UP in ev3.buttons.pressed():
                self.y.run(Pen.speed)
            elif Button.DOWN in ev3.buttons.pressed():
                self.y.run(-Pen.speed)
            else:
                self.y.run(0)

        # wait for buttons up
        while len(ev3.buttons.pressed()) > 0:
            pass

        # z manual calibration
        broken_press = False
        while Button.CENTER not in ev3.buttons.pressed():
            if Button.UP in ev3.buttons.pressed():
                self.z.run(-60)
                broken_press = True
            elif Button.DOWN in ev3.buttons.pressed():
                self.z.run(60)
                broken_press = True
            else:
                self.z.run(0)

        if broken_press:
            pen.up()

        self.x.reset_angle(0)
        self.y.reset_angle(0)
        self.z.reset_angle(0)
        

    def run_x(self, angle, wait=True):
        self.x.run_angle(Pen.speed, -angle, wait=wait)

    def run_y(self, angle, wait=True):        
        self.y.run_angle(Pen.speed * Pen.aspect, -angle * Pen.aspect, wait=wait)

    def reset(self):
        self.z.run_target(Pen.speed, 0)
        self.y.run_target(Pen.speed, 0, wait=False)
        self.x.run_target(Pen.speed, 0)

    def line(self, x, y):
        delta_x = x - self.x.angle()
        delta_y = y - self.y.angle()
    
        self.x.run_target(Pen.speed, x, wait=False)
        self.y.run_target(Pen.speed, y * Pen.aspect)
    
    def dot(self, x, y):
        self.y.run_target(Pen.speed, y * Pen.aspect)
        self.x.run_target(Pen.speed, x)
        self.down()
        self.up()




def print_image():
    pixel_size = 32

    with open("palette.json", "r") as palettefile:
        palette = load(palettefile)

    img = []
    with open("image.csv", "r") as csvfile:
        reader = reader(csvfile)
        for row in reader:
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

        ev3.light.on(Color.RED)
        ev3.screen.clear()
        ev3.screen.print(color["name"] + ": " + color["count"])

        while True:
            if len(ev3.buttons.pressed()) == 0:
                break
        skip = False
        while True:
            if Button.CENTER in ev3.buttons.pressed():
                break
            elif Button.UP in ev3.buttons.pressed():
                skip = True
                break
        if skip:
            continue

        ev3.light.on(Color.ORANGE)

        pen.dot(i * pixel_size, -100)

        for y, row in enumerate(img):
            if y % 2 == 0:
                for x, pixel in enumerate(row):
                    if pixel == i:
                        pen.dot(x * pixel_size, y * pixel_size)
            else:
                for x, pixel in reversed(list(enumerate(row))):
                    if pixel == i:
                        pen.dot(x * pixel_size, y * pixel_size)

pen = Pen()
pen.initialize()
print_image()
pen.reset()
    


    
