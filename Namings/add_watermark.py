from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from argparse import ArgumentParser
from change_time import change_time

def watermark_text(input_image_path: Path, output_image_path: Path, text):
    im = Image.open(input_image_path)
    _, height = im.size
    # make the image editable
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype('arial.ttf', height // 50)
    text_width, _ = draw.textsize(text, font)

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


supported_formats = ['*.jpg', '*.png']

if __name__ == '__main__':
    parser = ArgumentParser(description='Adds watermark to images.')
    parser.add_argument('-i', '--input', help='Input directory.')
    parser.add_argument('-o', '--output', help='Output directory.')
    parser.add_argument()
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
