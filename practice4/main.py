"""
    Chương trình clone source https://600tuvungtoeic.com/
"""

import os
import bs4
import requests
import shutil
import json
import codecs
import cv2

SOURCE_URL = 'https://600tuvungtoeic.com/'

idWord = 1


def main():
    r = requests.get(SOURCE_URL)
    if r.ok:
        s = bs4.BeautifulSoup(r.content, 'lxml')
        items = s.select('.gallery-item')
        listTopic = []
        listWord = []
        listWordError = []
        count = 1
        for item in items:
            count += 1
            data = {}
            print(
                '----------------------------------------------------------------------------------------------------------------------------------------')
            # print(item)
            page = item.select_one('a')
            page = page.attrs['href'] if page else ''

            topic_en = item.select_one('h3')
            topic_en = topic_en.text.strip() if topic_en else ''

            data['topic_en'] = topic_en.split(' - ')[1] if topic_en else ''
            data['id'] = int(topic_en.split(' - ')[0]) if topic_en else '0'

            # print(page)
            # print(str(data))

            image_url = item.select_one('img')
            image_url = image_url.attrs['src'] if image_url else ''

            data['image'] = downloadFile('topic_image', image_url, True)

            image_topic = 'topic_image/' + data['image']
            if not os.path.isdir('topic_image/image_unpass'):
                os.mkdir('topic_image/image_unpass')
            img = cv2.imread(image_topic, 0)
            data['image_unpass'] = data['image'].split('.')[0] + '_unpass.jpg'
            cv2.imwrite('topic_image/image_unpass/' + data['image_unpass'], img)

            topicDetail(page, data, listWord, listWordError)

            listTopic.append(data)

            print(
                '---------------------------------------------------------------------------------------------------------------------------------------')

            # if count == 5:
            #     break
        print(listTopic)
        print(listWord)
        dir = '600WordToiec'

        if not os.path.isdir(dir):
            os.mkdir(dir)

        topic = codecs.open(os.path.join(dir, 'Topic.json'), encoding='utf-8', mode='w')
        word = codecs.open(os.path.join(dir, 'Word.json'), encoding='utf-8', mode='w')
        wordError = codecs.open(os.path.join(dir, 'WordError.json'), encoding='utf-8', mode='w')
        json.dump(listTopic, topic, ensure_ascii=False, indent=2)
        json.dump(listWord, word, ensure_ascii=False, indent=2)
        json.dump(listWordError, wordError, ensure_ascii=False, indent=2)


def topicDetail(url, topic, listWord, listError):
    global idWord
    isError = False
    r = requests.get(os.path.join(SOURCE_URL, url))
    print(r.url)
    if r.ok:
        s = bs4.BeautifulSoup(r.content, 'lxml')

        topic_vi = s.select_one('h2.page-title')
        topic_vi = topic_vi.text.strip() if topic_vi else ''
        topic_vi = topic_vi.split(' - ')[-1]
        # print(topic_vi)
        topic['topic_vi'] = topic_vi

        items = s.select('.tuvung')

        for item in items:
            word = {'id': idWord, 'id_topic': topic['id']}

            contents = item.select('.noidung > span')
            if contents.__len__() == 0:
                continue
            vocabulary = contents[0].text.strip()
            vocabulary = vocabulary if vocabulary else ''
            word['vocabulary'] = vocabulary

            spelling = contents[1].text.strip()
            spelling = spelling if spelling else ''
            word['spelling'] = spelling

            contain_explain_vi = contents[3].next_sibling.strip()
            contain_explain_vi = contain_explain_vi if contain_explain_vi else ''

            from_type = contain_explain_vi.split(')')[0]
            from_type = from_type if from_type else ''
            word['from_type'] = from_type.strip() + ')'

            explain_vi = contain_explain_vi.split('):')[1]
            explain_vi = explain_vi if explain_vi else ''
            word['explain_vi'] = explain_vi.strip()

            try:
                explain_en = contents[2].next_sibling
                explain_en = explain_en if explain_en else ''
                if '<br/>' in str(explain_en):
                    if 'catalog' in word['vocabulary']:
                        explain_en = 'A complete list of items, typically one in alphabetical or other systematic order'
                    elif 'open to' in word['vocabulary']:
                        explain_en = 'To be receptive to or welcoming of something that comes from outside of oneself.'
                    elif 'broaden' in word['vocabulary']:
                        explain_en = 'Become larger in distance from side to side; widen.'
                    elif 'be ready for' in word['vocabulary']:
                        explain_en = 'feeling that you must have or must do something'
                    else:
                        example_en = ''
                        isError = True
                word['explain_en'] = explain_en
            except TypeError:
                continue

            try:
                example_en = contents[4].next_sibling.strip()
                example_en = example_en if example_en else ''
                word['example_en'] = example_en

                example_vi = item.select_one('.noidung > b')
                example_vi = example_vi.text.strip() if example_vi else ''
                word['example_vi'] = example_vi

                image_word = item.select_one('.hinhanh > img')
                image_word = image_word.attrs['src'] if image_word else ''
                if image_word:
                    if ' ' in image_word:
                        image_word = image_word.replace(' ', '_')
                    word['image'] = downloadFile('word_image', image_word, True)
                else:
                    isError = True

                audio = item.select_one('.noidung > audio > source')
                audio = audio.attrs['src'] if audio else ''
                if audio:
                    if ' ' in audio:
                        audio = audio.replace(' ', '_')
                    word['audio'] = downloadFile('audio', os.path.join(SOURCE_URL, audio))
                else:
                    isError = True
                    contentAudio = item.select_one('.noidung').contents[-1]
                    contentAudio = str(contentAudio) if contentAudio else ''
                    if contentAudio:
                        contentAudio = contentAudio.split('<audio')[1]
                        if contentAudio:
                            contentAudio = contentAudio.split('<source src="')[1]
                            if contentAudio:
                                contentAudio = contentAudio.split('" type')[0]
                                if ' ' in contentAudio:
                                    contentAudio = contentAudio.replace(' ', '_')
                                word['audio'] = downloadFile('audio', os.path.join(SOURCE_URL, contentAudio))
                                isError = False
                idWord += 1

                print(word)
                if isError:
                    isError = False
                    listError.append(word)
                else:
                    listWord.append(word)
            except Exception:
                pass


def downloadFile(dir, url, is_image=False):
    # tạo thư mục
    if not os.path.isdir(dir):
        os.mkdir(dir)

    file_name = url.split('/')[-1]
    if is_image:
        file_name = file_name.split('.')[0] + ".jpg"
    file_name = file_name.lower()
    if '-' in file_name:
        file_name = file_name.replace('-', "_")

    if os.path.exists(file_name):
        return file_name

    response = requests.get(url, stream=True)
    if response.status_code == 404:
        print('Error Not Found')
        print(url)
    with open(dir + '/' + file_name, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)

    return file_name


if __name__ == '__main__':
    main()
