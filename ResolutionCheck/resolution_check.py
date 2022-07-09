import re
from pathlib import Path
from PIL import Image
from argparse import ArgumentParser

supported_formats = ['.jpg', '.png']
resolution_re = re.compile('(\d+)\/(\d+)')
tolerance = 0.07

def parse_resolution(resolution: str) -> tuple[int, int]:
    match = resolution_re.match(resolution)
    if match is None:
        raise ValueError('Resolution is not valid')
    
    nums = match.groups()
    proportion = int(nums[0]) / int(nums[1])
    return proportion - tolerance, proportion + tolerance

def check(path: Path, resolution: tuple[int, int]):
    for supported_type in supported_formats:
        for img_path in path.glob(supported_type):
            with Image.open(img_path) as img:
                width, height = img.size
                actual_proportion = width / height
                if not (resolution[0] <= actual_proportion <= resolution[1]):
                        print(img_path.name)

if __name__ == '__main__':
    parser = ArgumentParser(description='Check resolution of images.')
    parser.add_argument('-d', '--directory', required=True ,help='Directory of image files.')
    parser.add_argument('-r', '--resolution', required=True, help='Resolution to check.')
    args = parser.parse_args()
    check(Path(args.directory), parse_resolution(args.resolution))
