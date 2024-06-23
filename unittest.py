from draw3r import *
from localsim import *

from pygame.locals import *

def test_main():
    drawer = Draw3r(VirtualHub(), VirtualPen())
    
    # test_image(drawer)
    test_path(drawer)

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