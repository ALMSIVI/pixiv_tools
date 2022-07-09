import os
from pathlib import Path
from win32_setctime import setctime
from argparse import ArgumentParser


def change_time(origin: Path, target: Path):
    stat = origin.stat()
    atime = stat.st_atime
    mtime = stat.st_mtime
    ctime = stat.st_ctime
    setctime(target, ctime)
    os.utime(target, (atime, mtime))

if __name__ == '__main__':
    parser = ArgumentParser(description='Changes creation time of file.')
    parser.add_argument('-o', '--origin', required=True, help='Original directory.')
    parser.add_argument('-t', '--target', required=True, help='Target directory.')
    args = parser.parse_args()

    origin = Path(args.origin)
    target = Path(args.target)

    for filename in origin.iterdir():
        change_time(filename, target / filename.name)
