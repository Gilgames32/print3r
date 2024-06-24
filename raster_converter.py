import csv
import json
from PIL import Image, ImageColor

sourcepath = ".img/ralsei2.png"

palettepath = "palette.json"
outpath = "image.csv"

mirror = False

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


def convert_image_to_array(image_path):
    # open in rgb
    image = Image.open(image_path)
    image = image.convert("RGB")

    if mirror:
        image = image.transpose(Image.FLIP_LEFT_RIGHT)

    # get pixels as indexes
    pixel_data = list(image.getdata())
    index_data = [get_color_index(pixel, load_palette()) for pixel in pixel_data]

    # convert to 2d array
    width, height = image.size
    index_array = [index_data[i : i + width] for i in range(0, len(index_data), width)]

    return index_array


def csv_writer(data):
    with open(outpath, "w", newline="\n") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)

def convert(path):
    index_array = convert_image_to_array(path)
    csv_writer(index_array)

def main():
    convert(sourcepath)
    print("Done!")


if __name__ == "__main__":
    main()
