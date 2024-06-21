from PIL import Image, ImageColor

hexpalette = [
    "#ffffff", # White
    "#cc2929", # Red
    "#e57a2e", # Orange
    "#f2d43d", # Yellow
    "#85cc3d", # Green
    "#268026", # Dark Green
    "#3399cc", # Blue
    "#1f3399", # Dark Blue
    "#823aa6", # Purple
    "#f255be", # Pink
    "#000000", # Black
]

rgbpalette = [ImageColor.getcolor(hexcolor, "RGB") for hexcolor in hexpalette]

def closest_color(color, palette):
    for i, palette_color in enumerate(palette):
        if color == palette_color:
            return i


def convert_image_to_array(image_path):
    image = Image.open(image_path)

    image = image.convert("RGB")

    pixel_data = list(image.getdata())

    index_data = [closest_color(pixel, rgbpalette) for pixel in pixel_data]

    width, height = image.size
    index_array = [index_data[i:i+width] for i in range(0, len(index_data), width)]

    return index_array


image_path = "debug1.png"
binary_array = convert_image_to_array(image_path)
print("[")
for row in binary_array:
    print("\t" + str(row) + ",")
print("]")