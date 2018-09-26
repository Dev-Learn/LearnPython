"""
    Chương trình tải các bài viết từ tuổi trẻ
"""
import bs4
import requests

SOURCE_URL = 'https://vnexpress.net/tin-tuc/khoa-hoc'

def get_content_detail(url):

    """
        Lấy content bài viết detail
    """

    print(url)

    data = {}
    r = requests.get(url)
    if r.ok:
        s = bs4.BeautifulSoup(r.content, 'lxml')
        title = s.select_one('h1')
        # print(title.text.strip() if title else '')
        data['title'] = title
        description = s.select_one('h2')
        # print(description.text.strip() if description else '')
        data['description'] = description
        content = s.select_one('article')
        # print(content.text.strip() if  content else '')
        data['content'] = description

    return data

def main():
    r = requests.get(SOURCE_URL)
    if r.ok:
        s = bs4.BeautifulSoup(r.content,'lxml')
        items = s.select('.list_news h3 > a')
        for item in items:
            if 'html#box_comment' in item.attrs['href']:
               pass
            else:
                article = get_content_detail(item.attrs['href'])
    else:
        print('Không truy cập được !!!')

if __name__ == '__main__':
    main()