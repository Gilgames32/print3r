from printerface import *

import csv
import json

class Draw3r:
    def __init__(self, hub: IHub, pen: IPen):
        self.hub = hub
        self.pen = pen

    def image(self, imagefile, palettefile):
        with open(palettefile, "r") as palettefile:
            palette = json.load(palettefile)

        img = []
        with open(imagefile, "r") as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                img.append([int(pixel) for pixel in row])

        # too much voodoo or divine intellect? call it
        flat_img = [pixel for row in img for pixel in row]

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

            self.hub.busy()

            self.pen.dotcoord(i, -2)

            for y, row in enumerate(img):
                erow = enumerate(row) if y % 2 == 0 else reversed(list(enumerate(row)))
                for x, pixel in erow:
                    if pixel == i:
                        self.pen.dotcoord(x, y)
    
    
    def path(self, pathfile):
        lines = []
        with open(pathfile, "r") as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                lines.append([int(coord) for coord in row])
        
        # TODO busy n shi

        for line in lines:
            self.pen.line(*line)

        