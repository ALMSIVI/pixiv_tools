import os
from PIL import Image

dir = input("Please input directory: ")
resolution = input("Please confirm resolution: 16/9 or 16/10: ")
files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f)) and (f.endswith('.jpg') or f.endswith('.png'))]
for f in files:
  with Image.open(os.path.join(dir, f)) as img:
    width, height = img.size
    if resolution == "16/9":
      if (width / height < 1.75 or width / height > 1.8):
        print(f)
    elif resolution == "16/10":
      if (width / height < 1.58 or width / height > 1.63):
        print(f)
    else:
      print("Resolution not supported")
