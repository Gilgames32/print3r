#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port, Color, Button
from pybricks.tools import wait


# brick
ev3 = EV3Brick()
ev3.light.on(Color.RED)


class Pen:
    speed = 512
    press = 90
    aspect = 1.6/2 # w/h
    y_deadangle = -60

    def __init__(self, x_port: Port = Port.A, y_port: Port = Port.B, z_port: Port = Port.C):
        self.x = Motor(x_port)
        self.y = Motor(y_port)
        self.z = Motor(z_port)
        self.y_dir = False

    def up(self):
        self.z.run_angle(Pen.speed, -Pen.press)

    def down(self):
        self.z.run_angle(Pen.speed, Pen.press)
    
    def initialize(self):
        broken_press = False
        while True:
            if Button.UP in ev3.buttons.pressed():
                self.z.run(50)
                broken_press = True
            elif Button.DOWN in ev3.buttons.pressed():
                self.z.run(-50)
                broken_press = True
            else:
                self.z.run(0)
            
            if Button.LEFT in ev3.buttons.pressed():
                self.x.run(Pen.speed)
            elif Button.RIGHT in ev3.buttons.pressed():
                self.x.run(-Pen.speed)
            else:
                self.x.run(0)
            
            if Button.CENTER in ev3.buttons.pressed():
                break

        if broken_press:
            pen.up()

        self.x.reset_angle(0)

        #self.y.run_angle(100, Pen.y_deadangle)
        #self.y.run_angle(100, -Pen.y_deadangle)
        self.y_dir = True
        self.y.reset_angle(0)

        self.z.reset_angle(0)
        


    def run_x(self, angle, wait=True):
        self.x.run_angle(Pen.speed, -angle, wait=wait)

    def run_y(self, angle, wait=True):
        # deadzone patch
        if self.y_dir and angle < 0:
            self.y.run_angle(Pen.speed, -Pen.y_deadangle)
            self.y_dir = False
        elif not self.y_dir and angle > 0:
            self.y.run_angle(Pen.speed, Pen.y_deadangle)
            self.y_dir = True
        
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



def print_w():
    pen.down()
    pen.run_y(300, wait=False)
    pen.run_x(300)
    pen.run_y(-300, wait=False)
    pen.run_x(300)
    pen.run_y(300, wait=False)
    pen.run_x(300)
    pen.run_y(-300, wait=False)
    pen.run_x(300)
    pen.up()

def print_square():
    pen.down()
    pen.run_y(300)
    pen.run_x(300)
    pen.run_y(-300)
    pen.run_x(-300)
    pen.up()

def print_square2():
    pen.down()
    pen.line(0, 400)
    pen.line(400, 400)
    pen.line(400, 0)
    pen.line(0, 0)
    pen.up()

def print_image():
    pixel_size = 32
    palette = [
        "White",
        "Red",
        "Orange",
        "Yellow",
        "Green",
        "Dark Green",
        "Blue",
        "Dark Blue",
        "Purple",
        "Pink",
        "Black",
    ]
    img = [
        [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10],
        [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10],
        [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10],
        [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10],
        [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10],
        [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10],
        [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10],
        [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10],
        [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10],
        [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10],
        [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10],
        [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10],
        [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10],
        [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10],
        [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10],
        [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10],
        [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10],
        [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10],
        [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10],
        [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10],
        [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10],
        [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10],
        [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10],
        [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10],
        [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10],
        [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10],
        [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10],
        [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10],
        [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10],
        [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 0, 0, 10, 10, 10, 10, 10, 10, 10, 10],
    ]
    for i, color in enumerate(palette):
        if color == "White":
            continue

        ev3.screen.clear()
        ev3.screen.draw_text(50, 50, color)

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
    


    
