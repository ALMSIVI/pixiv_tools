# Resolution Check

Checks if the pictures are wallpaper-sized.

- A small tolerance in resolution proportion is allowed; change the `tolerance` in the file.

- Pixiv supports only .jpg and .png pictures, so only these two are supported.

## Dependencies

pip required:

- PIL (Pillow)

## Running

```shell
python3 resolution_check.py -d <dir> -r <resolution>
```

The resolution should be formatted as `<number>/<number>`, for example, `16/9` or `3/2`.