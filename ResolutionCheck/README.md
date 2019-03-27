# Resolution Check

Checks if the pictures are wallpaper-sized (16/9 or 16/10).

- Resolutions are not absolute: for 16/9 (1.77778), the program accepts resolutions from 1.75 to 1.8. For 16/10 (1.6), the program accepts resolutions from 1.58 to 1.63.

- Pixiv supports only .jpg and .png pictures, so only these two are supported.

## Dependencies

pip required:

- PIL (Pillow)

## Running

```shell
python3 resolution_check.py
```

Enter the directory, and resolution.