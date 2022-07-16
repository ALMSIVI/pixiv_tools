import datetime
import json
import re
import webbrowser
from urllib.parse import urlencode

resolution_re = re.compile('(\d+)x(\d+)')

def parse_resolution(resolution: str) -> tuple[int, int]:
    match = resolution_re.match(resolution)
    if match is None:
        raise ValueError('Resolution is not valid')
    
    nums = match.groups()
    return int(nums[0]), int(nums[1])

if __name__ == '__main__':
    with open('link_config.json', 'rt', encoding='utf-8') as f:
        data = json.load(f)
    
    for resolution in data['resolutions']:
        width, height = parse_resolution(resolution)
        tag = data['keyword']
        o = data['offset']
        query = {
            'order': data['order'],
            'mode': data['mode'],
            'wlt': width - o,
            'wgt': width + o,
            'hlt': height - o,
            'hgt': height + o,
            'scd': data['last_update']
        }

        base_url = f'https://www.pixiv.net/en/tags/{tag}/artworks?'
        url = base_url + urlencode(query)
        webbrowser.open(url)

    data['last_update'] = str(datetime.date.today())

    with open('link_config.json', 'wt', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
