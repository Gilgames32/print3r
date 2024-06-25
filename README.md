# PRINT3R
(because i could not have come up with an edgier name)

the print3r is a lego plotter, a little side project i made in about a week

### functionalities:
- converting and printing raster images (tested with png, jpg)
- converting svg paths into lines using interpolation, then printing it
- converting is theoretically possible on the ev3 but its not recommended, i suggest you do it on your desktop

### specs:
- using the ev3dev official image with python 3.5.something :(, ev3dev2, numpy, pygame (for testing), svgpathtools
- uses A4 paper
- 10 colors + white
- time to print varies on method and complexity of the image (ie. its painfully slow lol)
- i used it at around 13 ppi but a higher ppi is theoretically possible
- that allowed me to do around 100x120 px images, huge top margin because of the wheels
- about 1-2 mm deadzone still after 4 versions :(

### experience:
- was happy to find out about pybricks, but micropython felt limited, moved to ev3dev
- ev3devs python is old, couldnt debug out of the box on the ev3, is possible theoretically though
- tried updating python or building it from source, wasted 2 days before giving up
- the ev3 is painfully slow, its a miracle ev3dev works
- lego parts were not meant for precision it turns out

### in action:
https://github.com/Gilgames32/print3r/assets/91968230/5f7be07c-7e0e-4731-a2c5-b668156df74b

### gallery:

#### vector:
![20240625_174140](https://github.com/Gilgames32/print3r/assets/91968230/64181789-d42c-4eca-99c0-7fc2d2939247)
![20240625_174157](https://github.com/Gilgames32/print3r/assets/91968230/53ac7193-d0db-414f-9473-030eeb32fd70)

#### pixel:
![20240625_174148](https://github.com/Gilgames32/print3r/assets/91968230/7aac056f-c7b3-4b48-af0e-cacd5addef00)
![20240625_174101](https://github.com/Gilgames32/print3r/assets/91968230/197e9366-0a82-4cd3-9b75-fe47461a8f6c)
![20240625_174051](https://github.com/Gilgames32/print3r/assets/91968230/1f0b4e3b-06dd-46e0-9380-605bd42164b0)

#### hexagonal:
![20240625_174016](https://github.com/Gilgames32/print3r/assets/91968230/95cd0859-5ff4-4a2f-b0bb-162ff8be9cd8)
