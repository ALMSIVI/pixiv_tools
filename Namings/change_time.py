import os
import pathlib
from win32_setctime import setctime
from argparse import ArgumentParser


def change_time(origin_filename, target_filename):
    origin = pathlib.Path(origin_filename).stat()

    atime = origin.st_atime
    mtime = origin.st_mtime
    ctime = origin.st_ctime
    setctime(target_filename, ctime)
    os.utime(target_filename, (atime, mtime))

if __name__ == '__main__':
    parser = ArgumentParser(description='Changes creation time of file.')
    parser.add_argument('-o', '--origin', required=True, help='Original directory.')
    parser.add_argument('-t', '--target', required=True, help='Target directory.')
    args = parser.parse_args()

    origin = args.origin
    target = args.target

    for filename in os.listdir(origin):
        change_time(os.path.join(origin, filename), os.path.join(target, filename))

        

