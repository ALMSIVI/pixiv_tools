import json
import webbrowser
import datetime

if __name__ == '__main__':
  with open('link_config.json', 'r+', encoding = 'utf-8') as f:
    data = json.load(f)
    for resolution in data['resolutions']:
      res_nums = resolution.split('x')
      url = 'https://www.pixiv.net/search.php?word={0}&order={1}&mode={2}&wlt={3}&wgt={3}&hlt={4}&hgt={4}&scd={5}'.format(data['keyword'], data['order'], data['mode'], res_nums[0], res_nums[1], data['last_update'])
      webbrowser.open(url)
    
    data['last_update'] = str(datetime.date.today())
    f.seek(0) # reset file position to beginning
    json.dump(data, f, ensure_ascii = False, indent = 2)
    f.truncate() # remove remaining part