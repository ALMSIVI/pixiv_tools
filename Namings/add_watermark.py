from PIL import Image, ImageDraw, ImageFont
import os
import pathlib
from win32_setctime import setctime
from argparse import ArgumentParser


def watermark_text(input_image_path, output_image_path, text):
    im = Image.open(input_image_path)
    width, height = im.size
    # make the image editable
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("arial.ttf", height // 50)
    text_width, text_height = draw.textsize(text, font)

    y = 0
    x = text_width + 10

    # Top
    # Black
    draw.text((0, y), text, fill=(0, 0, 0), font=font)
    # White
    draw.text((x, y), text, fill=(255, 255, 255), font=font)

    # Bottom
    y = height - height // 50
    # Black
    draw.text((0, y), text, fill=(0, 0, 0), font=font)
    # White
    draw.text((x, y), text, fill=(255, 255, 255), font=font)

    im.save(output_image_path)


def change_time(origin_filename, target_filename):
    origin = pathlib.Path(origin_filename).stat()

    atime = origin.st_atime
    mtime = origin.st_mtime
    ctime = origin.st_ctime
    setctime(target_filename, ctime)
    os.utime(target_filename, (atime, mtime))


if __name__ == '__main__':
    parser = ArgumentParser(description='Adds watermark to images.')
    parser.add_argument('-i', '--input', help='Input directory.')
    parser.add_argument('-o', '--output', help='Output directory.')
    args = parser.parse_args()

    inp = args.input

    output = args.output
    if not output:
        output = os.getcwd()

    if not os.path.isdir(output):
        os.mkdir(output)

    for image in os.listdir(inp):
        input_filename = os.path.join(inp, image)

        if os.path.isdir(os.path.join(inp, image)):
            continue

        image_split = image[:-4].split('_')
        image_id = image_split[-2] if image_split[-1].startswith(
            'p') else image_split[-1]

        output_filename = os.path.join(output, image)
        watermark_text(input_filename, output_filename, image_id)
        change_time(input_filename, output_filename)
