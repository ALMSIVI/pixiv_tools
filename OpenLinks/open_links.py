import json
import webbrowser
import datetime

if __name__ == '__main__':
    with open('link_config.json', 'r+', encoding='utf-8') as f:
        data = json.load(f)
        for resolution in data['resolutions']:
            res_nums = resolution.split('x')
            width = int(res_nums[0])
            height = int(res_nums[1])
            o = data['offset']
            url = f'https://www.pixiv.net/search.php?word={data["keyword"]}&order={data["order"]}&mode={data["mode"]}&wlt={width - o}&wgt={width + o}&hlt={height - o}&hgt={height + o}&scd={data["last_update"]}'
            webbrowser.open(url)

        data['last_update'] = str(datetime.date.today())
        f.seek(0)  # reset file position to beginning
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.truncate()  # remove remaining part
