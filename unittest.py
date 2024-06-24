from draw3r import *
from localsim import *
from svg_converter import convert as svg_convert
from raster_converter import convert as raster_convert

from pygame.locals import *

def test_main():
    # svg_convert(".img/aperture.svg", 4, 4)
    raster_convert(".img/flora.png")

    drawer = Draw3r(VirtualHub(), VirtualPen())
    
    test_image(drawer)
    # test_path(drawer)

    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

    pygame.quit()

def test_image(drawer):
    drawer.image("image.csv", "palette.json")

def test_path(drawer):
    drawer.path("path.csv")

def test_hexagonal(drawer):
    drawer.hexagonal()

if __name__ == "__main__":
    test_main()