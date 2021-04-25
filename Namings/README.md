# Naming scripts

So you have a library full of your favorite images from Pixiv. There are so many of them, so you want to hand-pick some of them and remove the others from your collection. However, you forgot to keep the ids of your work when you downloaded the images. The scripts here will help you match the images to their ids, and add watermarks on the images so you can easily navigate to the respective website next time you see the image.

---

First, you can use the plugin [Powerful Pixiv Downloader](https://chrome.google.com/webstore/detail/powerful-pixiv-downloader/dkndmhgdcmjdmkdonmbgjpijejdcilfh) to download your collection. There are a lot of parameters you can tune to your liking. If you do not feel like re-downloading your collection just to have their ids appended to the filenames, you can instead download your search result as a csv file, and use `rename_files.py` to rename your collection. It accepts two arguments: `-d` is your directory to your image collection, and `-f` is the filename of the csv file. It will assume that the original image files are in the format of **author_title**, and will try to match the author/title combination with the rows on the csv, and rename it to **author_title_authorID_titleID_pX**. However, there are several ways this might not be successful:

- The author has multiple works with the same title;
- The author has changed their name;
- The work has been removed.

In these occasions, you will need to do a manual match. You may consider using [this site](https://ascii2d.net/) to do an image match.

---

Once you have the ids in your filename, you can use `add_watermark.py` to add a watermark at the top left AND bottom left corner of the image. I did this because I am mainly using these scripts against my desktop background collection. In Windows, the taskbar is at the bottom, so I need watermarks at the top; in Mac, the taskbar is at the top, so I need watermarks at the bottom. The scripts accepts two arguments: `-i` for input directory, and `-o` for output directory. It will also attempt to change the creation/modified time of the newly created image to match the original image; for this, you need to install `win32_setctime` with pip. You can also use `change_time.py` to change the time of the file later on.