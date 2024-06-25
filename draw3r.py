from printerface import *

import csv
import json


class Draw3r:
    def __init__(self, hub: IHub, pen: IPen):
        self.hub = hub
        self.pen = pen

    def initialize(self):
        self.pen.initialize()

    def finalize(self):
        self.pen.up()
        self.pen.gohome()
        self.hub.title("Done. Empty deck?")
        if self.hub.choice():
            self.pen.empty()

    # draw path
    def path(self, pathfile):
        lines = []
        with open(pathfile, "r") as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                lines.append([int(coord) for coord in row])

        # TODO busy n shi
        self.pen.dotcoord(0, -5)

        for line in lines:
            self.pen.line(*line)

    # draw dots on a hexagonal grid
    def hexagonal(self, palettefile, imagefile):
        self.palettable(palettefile, imagefile, self.hexagonal_method)
        self.finalize()

    # draw dots on a pixel grid
    def pixel(self, palettefile, imagefile):
        self.palettable(palettefile, imagefile, self.pixel_method)
        self.finalize()

    def palettable(self, palettefile, imagefile, method):
        with open(palettefile, "r") as palettefile:
            palette = json.load(palettefile)

        img = []
        with open(imagefile, "r") as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                img.append([int(pixel) for pixel in row])

        # too much voodoo or divine intellect? call it
        flat_img = [pixel for row in img for pixel in row]

        adjustcount = 0
        for i in range(len(palette)):
            color = palette[str(i)]
            if i == 0:
                continue

            color["count"] = flat_img.count(i)
            if color["count"] == 0:
                continue

            self.hub.text(
                "Color\n" + color["name"] + "\nDots\n" + str(color["count"]),
                x=0,
                y=0,
                clear_screen=True,
            )
            self.hub.wait_no_presses()

            self.hub.waiting()

            if not self.hub.choice():
                continue

            self.pen.activecolor(color["hex"])

            self.pen.dotcoord(i + adjustcount, -2)
            self.pen.dotcoord(0, -2 - (i + adjustcount))
            # adjusting because the markers used arent the same...
            while not self.pen.adjust():
                self.pen.dotcoord(i + adjustcount, -2)
                self.pen.dotcoord(0, -2 - (i + adjustcount))
                adjustcount += 1

            self.hub.busy()

            method(img, i)

    def pixel_method(self, img, i):
        for y, row in enumerate(img):
            erow = enumerate(row) if y % 2 == 0 else reversed(list(enumerate(row)))
            for x, pixel in erow:
                if pixel == i:
                    self.pen.dotcoord(x, y)

    def hexagonal_method(self, img, i):
        for y, row in enumerate(img):
            ypos = y * 3 / 4
            if y % 2 == 0:
                for x, pixel in enumerate(row):
                    if pixel == i:
                        self.pen.dotcoord(x + 0.5, ypos)
            else:
                for x, pixel in reversed(list(enumerate(row))):
                    if pixel == i:
                        self.pen.dotcoord(x, ypos)
