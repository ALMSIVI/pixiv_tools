# Open Links

Opens picture search results in the browser for manual inspection. Automatically updates last inspection time such that users will always get the latest pictures. Supports multiple resolutions, mode and order (including premium only orders).

## Dependencies

None.

## Running

```python
python3 open_links.py
```

## Config

Use link_config.json for config.

### last_update

- Format: YYYY-MM-DD.
- Will get automatically updated each time the script is executed.

### resolutions

- An array of strings, formatted "AxB", where A and B are numbers indicating the width and height.

### keyword

- A string containing the keyword. Can use "OR" for multiple tags.

### mode

- A string specifying if r18 images will show up in the results. Options are 'safe' and 'r18'.

Below is a sample configuration of `link_config.json` for inspecting wallpapers. Notice that `order` is premium only.

```json
{
  "last_update": "2019-01-01",
  "resolutions": [
    "1920x1200",
    "1920x1080"
  ],
  "keyword": "keyword",
  "mode": "safe",
  "order": "popular_d"
}
```

