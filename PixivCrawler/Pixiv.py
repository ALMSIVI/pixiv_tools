import requests
import json
from bs4 import BeautifulSoup
from ParamParser import *
import time
import os

class Pixiv:
  def __init__(self):
    with open('config.json', encoding = 'utf-8') as config:
      self.config = json.load(config)
      # check fields that cannot be blank: keyword, email and password.
      # There is no check for inconsistent types.
      if self.config.get('email') == None or self.config.get('email') == '':
        self.err_callback('Email is not specified or is empty!')
      if self.config.get('password') == None or self.config.get('password') == '':
        self.err_callback('Password is not specified or is empty!')
      if self.config.get('keyword') == None or self.config.get('keyword') == '':
        self.err_callback('Keyword is not specified or is empty!')

      self.se = requests.session()
      self.headers = {
        'Referer': 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
      }
      #proxy
      if self.config.get('proxy', False):
        self.proxies = {
          'http': 'socks5h://127.0.0.1:1080',
          'https': 'socks5h://127.0.0.1:1080'
        }
      else:
        self.proxies = None

    with open('opts.json', encoding = 'utf-8') as opt:
      self.opts = json.load(opt)

    self.filters = {}
    self.params = {}

  def login(self):
    '''
    Login to pixiv in order to use advanced searching.
    '''
    base_url = 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'
    login_url = 'https://accounts.pixiv.net/api/login?lang=zh'
    post_key_html = self.se.get(base_url, headers = self.headers, proxies = self.proxies).text
    post_key_soup = BeautifulSoup(post_key_html, 'lxml')
    post_key = post_key_soup.find('input', {'name': 'post_key'})['value']
    data = {
        'pixiv_id': self.config['email'],
        'password': self.config['password'],
        'post_key': post_key
    }
    self.se.post(login_url, data = data, headers = self.headers, proxies = self.proxies)

  def search(self):
    '''
    Populates the params and performs the search.
    '''
    premium = self.config.get('premium', False)

    self.params[self.opts['keyword']['query_key']] = self.config[self.opts['keyword']['config_key']] # keyword
    # Selection params
    self.append_param('tag_mode', 'selection')
    if premium:
      self.append_param('order_premium', 'selection')
    else:
      self.append_param('order_not_premium', 'selection')

    self.append_param('type', 'selection')
    self.append_param('tool', 'selection')
    self.append_param('ratio', 'selection')
    self.append_param('mode', 'selection')

    # Number params
    self.append_param('min_width', 'number')
    self.append_param('max_width', 'number')
    self.append_param('min_height', 'number')
    self.append_param('max_height', 'number')
    if premium:
      self.append_param('min_bookmark', 'number')
      self.append_param('max_bookmark', 'number')
    else:
      self.set_bookmark_filter()

    # Date params
    self.append_param('start_time', 'date')
    self.append_param('end_time', 'date')

    # multi work filter
    self.filters['multi'] = self.config.get('download_multi', False)

    for i in range(self.config['start_page'], self.config['end_page'] + 1):
      self.params['p'] = i
      self.headers['Referer'] = 'https://www.pixiv.net/'
      url ='https://www.pixiv.net/search.php'
      html = self.se.get(url, headers = self.headers, params = self.params, timeout = 10, proxies = self.proxies)

      soup = BeautifulSoup(html.text, 'lxml')
      data_items = json.loads(soup.find('input', id = 'js-mount-point-search-result-list')['data-items'])

      return self.extract_work_info(data_items)


  def extract_work_info(self, data_items):
    '''
    Extracts information from the json.
    '''
    result = []
    count = 0
    for data_item in data_items:
      keep = True
      if self.filters.get('min') != None and data_item['bookmarkCount'] < self.filters['min']:
        keep = False
      if self.filters.get('max') != None and data_item['bookmarkCount'] > self.filters['max']:
        keep = False
      if self.filters['multi'] == False and data_item['pageCount'] > 1:
        keep = False
      if keep:
        url = data_item['url']
        begin = url.find('img/')
        end = url.find('_master')
        url_info = url[begin + 4:end - 3] # no real source here since there might be multi images

        result.append({
          'id': data_item['illustId'],
          'name': data_item['illustTitle'], # filename
          'username': data_item['userName'], # filename
          'url_info': url_info, # for fetching real source
          'count': data_item['pageCount'], # for fetching multiple images
          'type': data_item['illustType'] # for determining picture/ugoira
        })
        count += data_item['pageCount']
    return result, count

  def download_work(self, work):
    base_url = 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id='
    img_url = base_url + work['id']

    self.headers['Referer'] = img_url

    for i in range(work['count'] - 1):
      img_filename = work['name'] + '_' + work['username'] + '_' + str(i)
      # invalid characters
      img_filename = img_filename.replace('?', '-').replace('/', '-').replace('\\', '-').replace('*', '-') \
        .replace('|', '-').replace('>', '-').replace('<', '-').replace(':', '-').replace('"', '-').strip()

      if os.path.isfile('images/' + img_filename + '.png') or os.path.isfile('images/' + img_filename + '.jpg'):
          return

      # try jpg first, then png
      img_src = 'https://i.pximg.net/img-original/img/' + work['url_info'] + '_p' + str(i) + '.jpg'
      try:
        img = self.se.get(img_src, headers = self.headers, proxies = self.proxies).content
      except Exception:
        print('Download %s failed. Retrying...', img_filename)
        try:
          img = self.se.get(img_src, headers = self.headers, proxies = self.proxies).content
        except Exception:
          print('Download %s failed. Skipping image.' % img_filename)
          time.sleep(3)
          continue

      try:
        if img.decode('UTF-8').find('404 Not'):
          img_src = img_src[:-3] + 'png'
          try:
            img = self.se.get(img_src, headers = self.headers, proxies = self.proxies).content
          except:
            print('Download %s failed. Retrying...', img_filename)
            try:
              img = self.se.get(img_src, headers = self.headers, proxies = self.proxies).content
            except:
              print('Download %s failed. Skipping image.' % img_filename)
              time.sleep(3)
              continue

          with open('Download/' + img_filename + '.png', 'ab') as image:
            image.write(img)
            print('Downloaded %s' % img_filename)
          
      except:
        with open('Download/' + img_filename + '.jpg', 'ab') as image:
          image.write(img)
          print('Downloaded %s' % img_filename)

      time.sleep(3)

  def append_param(self, opt_key, opt_type):
    opt = self.opts[opt_key]
    result = ''
    if opt_type == 'selection':
      result = parse_selection(self.config[opt['config_key']], opt['correspondence'])
    elif opt_type == 'number':
      result = parse_number(self.config[opt['config_key']])
    elif opt_type == 'date':
      result = parse_date(self.config[opt['config_key']], opt['format'])

    if result != '':
      self.params[opt['query_key']] = result

  def set_bookmark_filter(self):
    min_bookmark = parse_num(self.config[self.opts['min_bookmark']['config_key']])
    if min_bookmark != '':
      self.filters['min'] = min_bookmark
    max_bookmark = parse_num(self.config[self.opts['max_bookmark']['config_key']])
    if min_bookmark != '':
      self.filters['max'] = max_bookmark

  def err_callback(self, message):
    print(message)
    input("Press any key to continue...")
    sys.exit()