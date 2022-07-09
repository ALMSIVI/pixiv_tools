import re
from csv import DictReader
from argparse import ArgumentParser
from pathlib import Path

def rename(directory: Path, filename: Path):
    with filename.open('rt') as csv:
        csv_reader = DictReader(csv)
        data = {}
        duplicates = set()
        for row in csv_reader:
            user, userId, title, titleId = row['user'], row['userId'], row['title'], row['\ufeffid']
            # Filter forbidden filename characters
            title = re.sub(r'[\\/*?:"<>|]', '_', title)
            # Comiket filters
            # if '@' in user:
            #     user = user[:user.index('@')]
            extension = row['fileName'][-3:]
            original_title = f'{user}_{title}.{extension}'
            #print(original_title)
            if original_title not in data and original_title not in duplicates:
                data[original_title] = f'{user}_{title}_{userId}_{titleId}.{extension}'
            else:
                data.pop(original_title, None)
                duplicates.add(original_title)

    marked = directory / 'Marked'
    marked.mkdir(exist_ok=True)

    for image in directory.iterdir():
        if not image.is_file():
            continue

        if image in data:
            # Rename
            image.replace(marked / data[image])


if __name__ == '__main__':
    parser = ArgumentParser(description='Rename image files given csv data.')
    parser.add_argument('-d', '--directory', required=True ,help='Directory of image files.')
    parser.add_argument('-f', '--filename', required=True, help='Path to the csv data file.')
    args = parser.parse_args()
    rename(Path(args.directory), Path(args.filename))
