# Pixiv Crawler

Crawls pictures from the site. Supports a range of custom options, including premium-only options.

Referred to from https://github.com/leniumC/pixiv-crawler.

## Dependencies

pip needed:

- requests[socks]
- beautifulsoup4
- lxml
- python-dateutil

## Running

```pyhon
python3 main.py
```

## opts.json

The correspondence is stored in opts.json. Use `null` to ignore the option.
##### keyword

- Specifies the keyword.
- Corresponds to 'word' in query.
- **Cannot be blank or null.**

##### tag_mode
- Specifies whether to match partial tag, full tag, or title & caption. Available in "Search Tools".
- Corresponds to 's_mode' in query.
- null or 'tag': partial tag. 's_tag' will not be set.
- 'full': tag (perfect matching). Will set s_mode to 's_tag_full'.
- 'tc': title or caption. Will set s_mode to 's_tc'.
#####order

- Specifies the order of the results: newest, oldest, or by popularity (all, male, female). Sorting by popularity is only available if `premium` is set to `true`. If popular is specified when `premium` is `false`, the default 'newest' will be used.
- Corresponds to 'order' in query.
- null or 'newest': sort by newest. 'order' will not be set.
- 'oldest': sort by oldest. Will set 'order' to 'date'.
- 'popular_all': Sort with popularity (with all). Will set order to 'popular_d'. **Premium only.**
- 'popular_male': Sort with popularity (male). Will set order to 'popular_male_d'. **Premium only.**
- 'popular_female': Sort with popularity (female). Will set order to 'popular_female_d'. **Premium only.**

##### type

- Specifies if illustration/manga/ugoira will be included. Available in "Search Tools".
- Corresponds to 'type' in query.
- null or 'all': include everything (illustration + manga + ugoira). 'type' will not be set.
- 'illustration': include illustrations only. Will set type to 'illust'.
- 'manga': include manga only. Will set type to 'manga'.
- 'ugoira': include ugoira (moving illustrations) only. Will set type to 'ugoira'. **Currently not supported. Will NOT be downloaded.**

##### tool

- Specifies the tool used to create the work: SAI, Photoshop, CLIP STUDIO PAINT, IllustStudio, ComicStudio. Available in "Search Tools".
- Corresponds to 'tool' in query.
- null or 'all': all production tools.  'tool' will not be set.
- 'sai': SAI. Will set 'tool' to 'SAI'.
- 'photoshop': Photoshop. Will set 'tool' to 'Photoshop'.
- 'csp': CLIP STUDIO PAINT. Will set 'tool' to 'CLIP STUDIO PAINT'.
- 'illust': IllustStudio. Will set 'tool' to 'IllustStudio'.
- 'comic': ComicStudio. Will set 'tool' to 'ComicStudio'.

##### ratio

- Specifies the ratio of the work: horizontal, vertical, square. Available in "Search Tools".
- Corresponds to 'ratio' in query.
- null or 'all': all aspect ratios. 'ratio' will not be set.
- 'horizontal': horizontal works only. Will set 'ratio' to '0.5'. *In fact, any number between 0 and 0.5 would do.*
- 'vertical': vertical works only. Will set 'ratio' to '-0.5'. *In fact, any number between -0.5 and 0 would do.*
- 'square': square works only. Will set 'ratio' to '0'.

##### mode

- Specifies if general/r18 works will be included.
- Corresponds to 'mode' in query.
- null or 'all': All works will be included. 'mode' will not be set.
- 'general': General (safe) works will be included. Will set 'mode' to 'safe'.
- 'r18': r18 (nsfw) works will be included. Will set 'mode' to 'r18'.

##### min_width

- Specifies the min width of the works. Available in "Search Tools" but the option there is imprecise.
- Corresponds to 'wlt' in query.

##### max_width

- Specifies the max width of the works. Available in "Search Tools" but the option there is imprecise.
- Corresponds to 'wgt' in query.

##### min_height

- Specifies the min height of the works. Available in "Search Tools" but the option there is imprecise.
- Corresponds to 'hlt' in query.

##### max_height

- Specifies the max height of the works. Available in "Search Tools" but the option there is imprecise.
- Corresponds to 'hgt' in query.

##### min_bookmark

- Specifies the minimum bookmarks that will be included.
- **Premium members are able to filter by bookmarks (from the server side). If `premium` is set to true, this functionality will be used; if not, a client side filter would be needed, and the number of works fetched may be fewer than expected.**

- Corresponds to 'blt' in query. **Premium only.**

##### max_bookmark

- Specifies the maximum bookmarks that will be included.

- **Premium members are able to filter by bookmarks (from the server side). If `premium` is set to true, this functionality will be used; if not, a client side filter would be needed, and the number of works fetched may be fewer than expected.**

- Corresponds to 'bgt' in query. **Premium only.**

##### start_time

- Specifies the start time of the works.

- Corresponds to 'scd' in query.
- Exact dates can be entered ([dateutil](https://dateutil.readthedocs.io/en/stable/) will be used to parse the date), or relative dates can be entered.
- 'Xd': X days ago.
- 'Xw': X weeks ago.
- 'Xm': X months ago.
- 'Xy': X years ago.
- The above four can be combined, and can be used more than once.

##### end_time

- Specifies the end time of the works.

- Corresponds to 'ecd' in query.
- Exact dates can be entered ([dateutil](https://dateutil.readthedocs.io/en/stable/) will be used to parse the date), or relative dates can be entered.
- 'Xd': X days ago.
- 'Xw': X weeks ago.
- 'Xm': X months ago.
- 'Xy': X years ago.
- The above four can be combined, and can be used more than once.

##### start_page

- Specifies the start page for searching.
- If set to null, will default at page 1.

##### end_page

- Specifies the end page for searching.
- If set to null, will default at page 5.

##### download_multi

- Specifies if multi-image works will be downloaded.
- If set to null, will default to false.

##### proxy

- boolean value specifying whether a socks 5 proxy will be used.
- If set to null, proxy will not be used.

##### premium

- boolean value specifying whether the user is a Pixiv Premium member. Premium member can use "Sort by popularity" and "Filter by bookmarks".
- If set to null, the user will be assumed not to have premium.

##### email

- Login email for the user.
- **Cannot be blank or null.**

##### password

- Login password for the user.
- **Cannot be blank or null.**



Below is a sample configuration of `Pixiv.json` for downloading wallpapers.


```json
{
  "keyword": "abc",
  "tag_mode": null,
  "order": "newest",
  "type": null,
  "tool": null,
  "ratio": null,
  "min_width": 1920,
  "max_width": 1920,
  "min_height": 1080,
  "max_height": 1080,
  "mode": "safe",
  "min_bookmark": 1000,
  "max_bookmark": 4999,
  "start_time": "1d",
  "end_time": null,

  "start_page": 1,
  "end_page": 2,

  "proxy": true,
  "premium": true,
  "email": "abc@def.ghi",
  "password": "abcdefghi"
}
```