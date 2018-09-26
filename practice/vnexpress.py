"""
    Chương trình tải các bài viết từ tuổi trẻ
"""
from pip._vendor import requests

SOURCE_URL = 'https://vnexpress.net/tin-tuc/khoa-hoc'

def main():
    r = requests.get(SOURCE_URL)
    if r.ok:
        print(r.content)
    else:
        print('Không truy cập được !!!')

if __name__ == '__main__':
    main()