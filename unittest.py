from draw3r import *
from localsim import *
from svg_converter import svg_convert
from raster_converter import raster_convert, hexagonal_convert

from pygame.locals import *

def test_main():
    # svg_convert(".img/aperture.svg", 4, 4)
    # raster_convert(".img/flora.png")
    # hexagonal_convert(".img/michi_dithered.png", 64)

    drawer = Draw3r(VirtualHub(), VirtualPen())
    
    test_hexagonal(drawer)
    # test_pixel(drawer)

    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

    pygame.quit()



def test_path(drawer):
    drawer.path("path.csv")

def test_hexagonal(drawer):
    drawer.hexagonal("palette.json", "image.csv")

def test_pixel(drawer):
    drawer.pixel("palette.json", "image.csv")

if __name__ == "__main__":
    test_main()