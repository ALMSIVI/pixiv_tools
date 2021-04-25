import os
import re
from csv import DictReader
from argparse import ArgumentParser

def rename(directory, filename):
    with open(filename, 'rt') as csv:
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

    try:
        os.mkdir(os.path.join(directory, 'Marked'))
    except:
        # File already exists, skip
        pass

    images = [image for image in os.listdir(directory) if os.path.isfile(os.path.join(directory, image))]
    for image in images:
        if image in data:
            # Rename
            os.rename(os.path.join(directory, image), os.path.join(directory, 'Marked', data[image]))


if __name__ == '__main__':
    parser = ArgumentParser(description='Rename image files given csv data.')
    parser.add_argument('-d', '--directory', required=True ,help='Directory of image files.')
    parser.add_argument('-f', '--filename', required=True, help='Path to the csv data file.')
    args = parser.parse_args()
    rename(args.directory, args.filename)