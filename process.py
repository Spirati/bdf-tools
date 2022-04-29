from io import BufferedReader
from typing import List, Any

from PIL import Image
from sys import argv
from math import sqrt, ceil


def read_to_property(file: BufferedReader, property: str, cast = None) -> List[Any]:
    line = ""
    while line.split(" ")[0] != property:
        line = file.readline()[:-1]
    output = line.split(" ")
    if len(output) > 1:
        output = output[1:]
        if cast:
            output = list(map(cast, output))
    if len(output) == 1:
        output = output[0]
    return output

def parse_font(path: str):
    with open(path) as file:
        bx, by, ox, oy = read_to_property(file, "FONTBOUNDINGBOX", int)

        family_name = read_to_property(file, "FAMILY_NAME").replace('"', "")
        weight_name = read_to_property(file, "WEIGHT_NAME").replace('"', "")
        output_name = family_name + weight_name

        chars = read_to_property(file, "CHARS", int)
        image_size = ceil(sqrt(chars))
        
        im = Image.new("RGBA", (bx*image_size, by*image_size), (255, 255, 255, 0))

        with open(f"{output_name}_atlas", "w") as atlas:
            atlas.write(f"{image_size} {bx} {by}\n")

            for index in range(chars):
                cx, cy = index % image_size, index // image_size
                char_point = read_to_property(file, "ENCODING")
                atlas.write(char_point + " ")
                bbx, bby, box, boy = read_to_property(file, "BBX", int)
                extra_bits = 8*ceil(bbx/8) - bbx
                read_to_property(file, "BITMAP")
                for y in range(bby):
                    num = int(file.readline(), 16) >> extra_bits
                    for x in range(bbx)[::-1]:
                        im.putpixel((bx*cx + x, by*cy + y), (255, 255, 255, 255*(num & 1)))
                        num >>= 1
        im.save(f"{output_name}.png")



if __name__ == "__main__":
    parse_font(argv[1])

