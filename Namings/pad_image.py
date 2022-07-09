from PIL import Image
from pathlib import Path
from argparse import ArgumentParser
from change_time import change_time

screen_sizes = {
    'air': 2560 / 1664,
    'pro14': 3024 / 1964,
    'pro16': 3456 / 2234,
}

def pad_image(input_image_path: Path, output_image_path: Path, type: str):
    im = Image.open(input_image_path)
    width, height = im.size
    
    new_height = round(width / screen_sizes[type])
    new_im = Image.new(im.mode, (width, new_height))
    new_im.paste(im, (0, new_height - height))
    new_im.save(output_image_path)


supported_formats = ['.jpg', '.png']

if __name__ == '__main__':
    parser = ArgumentParser(description='Pad the images to fit the new Macbook screens.')
    parser.add_argument('-i', '--input', help='Input directory.')
    parser.add_argument('-o', '--output', help='Output directory.')
    parser.add_argument('-t', '--type', help='Type of your Macbook.')
    args = parser.parse_args()

    in_path = Path(args.input)
    out_path = Path(args.output) if args.output else Path.cwd()
    out_path.mkdir(exist_ok=True)

    for image in in_path.iterdir():
        if not image.is_file() or image.suffix not in supported_formats:
            continue

        image_out = out_path / image.name
        pad_image(image, image_out, args.type)
        change_time(image, image_out)
