from printerface import *

import pygame

class VirtualHub:
    def busy(self):
        print("Busy...")

    def waiting(self):
        print("Waiting for input...")

    def wait_no_presses(self):
        print("Waiting for key release...")

    def choice(self):
        return True
        

    def title(self, text):
        self.text(text)

    def text(self, text, x=0, y=0, clear_screen=False):
        print(text)


class VirtualPen:
    DOTSIZE = 3
    TOPLEFT = (100, 100)
    SIMSCALE = 1/10

    def __init__(self):
        pygame.init()
        window_size = (800, 800)  # Set window size
        self.screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption('Virtual Print3r')
        self.screen.fill((255, 255, 255))
        self.pencolor = (0, 0, 0)

    def activecolor(self, hexa):
        self.pencolor = pygame.Color(hexa)

    def up(self):
        print("Pen up")

    def down(self):
        print("Pen down")

    def initialize(self):
        print("Pen initialized")

    def dotcoord(self, x, y):
        x = x * VirtualPen.DOTSIZE*2 + VirtualPen.TOPLEFT[0]
        y = y * VirtualPen.DOTSIZE*2 + VirtualPen.TOPLEFT[1]
        pygame.draw.circle(self.screen, self.pencolor, (x, y), VirtualPen.DOTSIZE)

    def line(self, x1, y1, x2, y2):
        x1 = x1 * VirtualPen.SIMSCALE + VirtualPen.TOPLEFT[0]
        y1 = y1 * VirtualPen.SIMSCALE + VirtualPen.TOPLEFT[1]
        x2 = x2 * VirtualPen.SIMSCALE + VirtualPen.TOPLEFT[0]
        y2 = y2 * VirtualPen.SIMSCALE + VirtualPen.TOPLEFT[1]
        pygame.draw.line(self.screen, self.pencolor, (x1, y1), (x2, y2))

    def gohome(self):
        print("Pen returned to home")
        pass

    def empty(self):
        print("Deck emptied")

    def adjust(self):
        return True

