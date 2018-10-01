"""
    Chương trình clone source https://600tuvungtoeic.com/
"""

import os
import bs4
import requests
import json
import codecs
import arrow

SOURCE_URL = 'https://600tuvungtoeic.com/'

def main():
    r = requests.get(SOURCE_URL)
    if r.ok:
        s = bs4.BeautifulSoup(r.content, 'lxml')
        print(s)
        items = s.select('.gallery-item')
        data = {}
        for item in items:
            print('----------------------------------------------------------------------------------------------------------------------------------------')
            # print(item)
            page = item.select_one('a')
            page = page.attrs['href'] if page else ''

            image = item.select_one('img')
            data['image'] = image.attrs['src'] if image else ''

            title = item.select_one('h3')
            title = title.text.strip() if title else ''

            data['title'] = title.split(' - ')[1] if title else ''
            data['id'] = title.split(' - ')[0] if title else ''

            print(page)
            print(str(data))

            print('----------------------------------------------------------------------------------------------------------------------------------------')

if __name__ == '__main__':
    main()