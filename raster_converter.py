import csv
import json
import numpy as np
import math
from PIL import Image, ImageColor

sourcepath = ".img/ralsei2.png"

palettepath = "palette.json"
outpath = "image.csv"

def load_palette():
    with open(palettepath, "r") as palettefile:
        palette = json.load(palettefile)

    for color in palette:
        palette[color]["rgb"] = ImageColor.getcolor(palette[color]["hex"], "RGB")

    return palette


def get_color_index(color, palette):
    for index, palette_color in palette.items():
        if color == palette_color["rgb"]:
            return int(index)
    return 0

def closestcolor(color, palette):
    color = np.array(color)
    distances = np.sqrt(np.sum((palette-color)**2,axis=1))
    index_of_smallest = np.where(distances==np.amin(distances))
    index_of_smallest = index_of_smallest[0][0]
    return palette[index_of_smallest]


def csv_writer(data):
    with open(outpath, "w", newline="\n") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)

def raster_convert(image_path, resize=False, outwidth=64):
    # open in rgb
    image = Image.open(image_path)
    image = image.convert("RGB")
    if resize:
        outheight = int(outwidth * image.size[1] / image.size[0])
        image = image.resize((outwidth, outheight), Image.ANTIALIAS)

    # get pixels as indexes
    pixel_data = list(image.getdata())
    palettedict = load_palette()
    rgbpalette = [palettedict[color]["rgb"] for color in palettedict]

    index_data = [get_color_index(closestcolor(pixel, rgbpalette), palettedict) for pixel in pixel_data]

    # convert to 2d array
    outwidth, outheight = image.size
    index_array = [index_data[i : i + outwidth] for i in range(0, len(index_data), outwidth)]
    csv_writer(index_array)


def rectangle_corners(center, sx, sy):
    x = center[0]
    y = center[1]

    corners = [
        (x - 0.5, y - 0.5),
        (x + 0.5, y - 0.5),
        (x + 0.5, y + 0.5),
        (x - 0.5, y + 0.5)
    ]

    return [(c[0] * sx, c[1] * sy) for c in corners]


def hexagonal_convert(image_path, outwidth=64):
    # open in rgb
    image = Image.open(image_path)
    image = image.convert("RGB")
    imgarray = np.asarray(image)

    outheight = int(outwidth * image.size[1] / image.size[0] * 4/3) 

    sx, sy = (image.size[0] / outwidth, image.size[1] / outheight)

    indexarray = []
    palettedict = load_palette()
    rgbpalette = [palettedict[color]["rgb"] for color in palettedict]

    for y in range(outheight):
        row = []
        for x in range(outwidth):
            raw = rectangle_corners((x + y % 2 * 0.5, y), sx, sy)
            r = []
            for points in raw:
                np0 = int(np.clip(points[0], 0, image.size[0]))
                np1 = int(np.clip(points[1], 0, image.size[1]))
                r.append((np0,np1))    
            
            color = np.average(imgarray[r[0][1]:r[3][1],r[0][0]:r[1][0]], axis=(0,1))    
            color = tuple([int(c) if not math.isnan(c) else 0 for c in color])
            row.append(get_color_index(closestcolor(color, rgbpalette), palettedict))
        indexarray.append(row)
    
    csv_writer(indexarray)

def main():
    raster_convert(sourcepath)
    print("Done!")


if __name__ == "__main__":
    main()
