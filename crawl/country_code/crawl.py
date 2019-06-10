import os
import bs4
import requests
import shutil
import json
import codecs
import cv2


SOURCE_URL = 'https://www.vnnic.vn/tenmien/hotro/danh-s%C3%A1ch-t%C3%AAn-t%C3%AAn-vi%E1%BA%BFt-t%E1%BA%AFt-c%E1%BB%A7-c%C3%A1c-qu%E1%BB%91c-gia-tr%C3%AAn-th%E1%BA%BF-gi%E1%BB%9Bi?lang=en'

def main():
    r = requests.get(SOURCE_URL)
    if r.ok:
        s = bs4.BeautifulSoup(r.content, 'lxml')
        print(s)


if __name__ == '__main__':
    main()