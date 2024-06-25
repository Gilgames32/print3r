#!/usr/bin/env python3

from time import sleep

from draw3r import Draw3r
from print3r import Brick, Pen

drawer = Draw3r(Brick(), Pen())

drawer.initialize()
drawer.hexagonal("palette.json", "image.csv")
# drawer.path("path.csv")
# drawer.pixel("palette.json", "image.csv")
drawer.finalize()

sleep(1)
