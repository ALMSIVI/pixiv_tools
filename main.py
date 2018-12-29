import requests
import json

import os
import shutil
from bs4 import BeautifulSoup

from Pixiv import Pixiv
def main():
  #site = input("Enter the site to crawl (p for Pixiv): ")
  
  pixiv = Pixiv()
  pixiv.login()
  work_info, count = pixiv.search()
  print('Fetched %d works consisting of %d pictures' % (len(work_info), count))

  try:
    os.mkdir('Download')
    for work in work_info:
      pixiv.download_work(work)
  except os.error:
    pass


if __name__ == '__main__':
  main()