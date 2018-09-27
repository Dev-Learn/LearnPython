"""
    Chương trình tải các bài viết từ tuổi trẻ
"""
import bs4
import requests
import json
import codecs
import arrow

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
        data['title'] = title.text.strip() if title else ''

        description = s.select_one('h2')
        # print(description.text.strip() if description else '')
        data['description'] = description.text.strip() if description else ''

        content = s.select_one('article.content_detail.fck_detail.width_common.block_ads_connect')
        # print(content.prettify() if  content else '')
        data['content'] = content.prettify() if content else ''

        pub_date = s.select_one('span.time.left')
        pub_date = pub_date.text.replace(' (GMT+7)','').split(',')[1] + pub_date.text.replace(' (GMT+7)','').split(',')[2] if  pub_date else ''
        # print(pub_date.text.strip() if  pub_date else '')
        print(pub_date.strip().split('/'))
        # if pub_date.strip().split('/')[1].strip().__len__() == 1 and pub_date.split('/')[0].strip().__len__() == 2:
        #     pub_date = arrow.get(pub_date,'DD/M/YYYY HH:mm').replace(tzinfo='Asia/Ho_Chi_Minh')
        # elif pub_date.strip().split('/')[1].strip().__len__() == 2 and pub_date.split('/')[0].strip().__len__() == 1:
        #     pub_date = arrow.get(pub_date, 'D/MM/YYYY HH:mm').replace(tzinfo='Asia/Ho_Chi_Minh')
        # elif pub_date.strip().split('/')[1] if pub_date.strip().split('/')[1].strip().__len__() == 1 else '' and pub_date.split('/')[0].strip().__len__() == 1:
        #     pub_date = arrow.get(pub_date, 'D/M/YYYY HH:mm').replace(tzinfo='Asia/Ho_Chi_Minh')
        # else:
        #     pub_date = arrow.get(pub_date, 'DD/MM/YYYY HH:mm').replace(tzinfo='Asia/Ho_Chi_Minh')
        # data['pub_date'] = pub_date.format(locale='vi')

    return data


def main():
    r = requests.get(SOURCE_URL)
    if r.ok:
        s = bs4.BeautifulSoup(r.content, 'lxml')
        items = s.select('.list_news h3 > a')
        for item in items:
            if 'html#box_comment' in item.attrs['href']:
                pass
            else:
                article = get_content_detail(item.attrs['href'])
                # # print(article)
                # file_name = arrow.get(article['pub_date']).format('DD-MM-YYYY HH-mm')
                # f = codecs.open(file_name + '.json', encoding='utf-8', mode='w')
                # json.dump(article, f, ensure_ascii=False,indent=2)

    else:
        print('Không truy cập được !!!')


if __name__ == '__main__':
    main()
