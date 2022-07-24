from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from argparse import ArgumentParser
from change_time import change_time


spacing = 10
supported_formats = ['.jpg', '.png']


def draw_text(draw, start_x, y, text_width, text, font):
    # Black
    draw.text((start_x, y), text, fill=(0, 0, 0), font=font)
    # White
    draw.text((start_x + text_width + spacing, y), text, fill=(255, 255, 255), font=font)


def watermark_text(input_image_path: Path, output_image_path: Path, text: str):
    im = Image.open(input_image_path)
    width, height = im.size
    # make the image editable
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype('arial.ttf', height // 50)
    text_width = draw.textlength(text, font)

    # Top left
    draw_text(draw, 0, 0, text_width, text, font)
    
    # Top right
    right_x = width - 2 * text_width - spacing
    draw_text(draw, right_x, 0, text_width, text, font)

    # Bottom left
    bottom_y = height - height // 50
    draw_text(draw, 0, bottom_y, text_width, text, font)

    # Bottom right
    draw_text(draw, right_x, bottom_y, text_width, text, font)

    im.save(output_image_path)


if __name__ == '__main__':
    parser = ArgumentParser(description='Adds watermark to images.')
    parser.add_argument('-i', '--input', help='Input directory.')
    parser.add_argument('-o', '--output', help='Output directory.')
    args = parser.parse_args()

    in_path = Path(args.input)
    out_path = Path(args.output) if args.output else Path.cwd()
    out_path.mkdir(exist_ok=True)

    for image in in_path.iterdir():
        if not image.is_file() or image.suffix not in supported_formats:
            continue

        image_split = image.stem.split('_')
        image_id = image_split[-2] if image_split[-1].startswith('p') else image_split[-1]

        image_out = out_path / image.name
        watermark_text(image, image_out, image_id)
        change_time(image, image_out)
