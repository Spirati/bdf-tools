from PIL import Image, ImageOps
from sys import argv

def write_character(font: Image.Image, image: Image.Image, cx: int, cy: int, x: int, y: int, bx: int, by: int):
    image.paste(font.crop((cx*bx, cy*by, (cx+1)*bx, (cy+1)*by)), (x*bx, by*y))

def write_text(text: str, font: str):
    with open(f"{font}_atlas") as af:
        size, bx, by = map(int, af.readline().split(" "))
        atlas = list(map(int, af.readline().split(" ")[:-1]))
    font_image = Image.open(f"{font}.png")
    im = Image.new("RGBA", (len(text)*bx, by))

    line_index = 0
    offset = 0
    max_offset = -1

    for char in text:
        if char == "\n":
            line_index += 1
            im = ImageOps.pad(im, (len(text)*bx, by*(line_index+1)), centering = (0, 0))
            if offset > max_offset:
                max_offset = offset
            offset = 0
            continue
        code = ord(char)
        code_index = atlas.index(code)
        cx, cy = code_index % size, code_index // size
        write_character(font_image, im, cx, cy, offset, line_index, bx, by)
        offset += 1
    if offset > max_offset:
        max_offset = offset
    im.crop((0, 0, bx*max_offset, by*(line_index+1))).save("out.png")

if __name__ == "__main__":
    write_text(argv[2], argv[1])