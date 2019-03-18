import pymysql.cursors
import os
import codecs
import json

# Kết nối vào database.
connection = pymysql.connect(host='localhost',
                             user='root',
                             db='toiec',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)


def openJson(path, isTopic):
    if not os.path.isfile(path):
        print('Không tìm thấy file : %s' % path)
    else:
        data = json.load(codecs.open(path, mode='r', encoding="utf8"))
        try:
            mycursor = connection.cursor()
            if isTopic:
                mycursor.execute(
                    'CREATE TABLE IF NOT EXISTS topic (id INT PRIMARY KEY, topic_en VARCHAR(255), topic_vi VARCHAR(255), image VARCHAR(255), image_unpass VARCHAR(255))')
                for item in data:
                    sql = 'INSERT INTO topic (id, topic_en,topic_vi,image,image_unpass) VALUES (%s, %s, %s, %s, %s)'
                    val = (item['id'], item['topic_en'], item['topic_vi'], item['image'].replace('jpg', 'webp'),
                           item['image_unpass'].replace('jpg', 'webp'))
                    mycursor.execute(sql, val)
                    connection.commit()
            else:
                mycursor.execute(
                    """CREATE TABLE IF NOT EXISTS word (id INT PRIMARY KEY, id_topic INT ,vocabulary VARCHAR(255),spelling VARCHAR(255)
                    ,from_type VARCHAR(255),explain_vi VARCHAR(255),explain_en VARCHAR(255),example_en VARCHAR(255),example_vi VARCHAR(255)
                    ,image VARCHAR(255),audio VARCHAR(255))""")
                for item in data:
                    sql = """INSERT INTO word (id, id_topic,vocabulary,spelling,from_type,explain_vi,explain_en,example_en,example_vi,image,audio) 
                              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                    val = (item['id'], item['id_topic'], item['vocabulary'], item['spelling'], item['from_type'],
                           item['explain_vi']
                           , item['explain_en'], item['example_en'], item['example_vi'],
                           item['image'].replace('jpg', 'webp'), item['audio'])
                    mycursor.execute(sql, val)
                    connection.commit()
        finally:
            connection.close()


def getExampleGame(vocabulary, text):
    print(vocabulary)
    print(text)
    if vocabulary in text:
        # print(textReplaceSuccess)
        list = text.split(vocabulary)
        # print(list)
        if list[1]:
            if ',' == list[1][0]:
                textReplaceSuccess = ''
                if ' ' in vocabulary:
                    print(vocabulary)
                    textReplace = vocabulary.split(' ')
                    for idx, itemString in enumerate(textReplace):
                        textReplaceSuccess += itemString.replace(itemString, '_' * len(itemString))
                        if idx < len(textReplace) - 1:
                            textReplaceSuccess += ' '
                if '' == textReplaceSuccess:
                    return text.replace(vocabulary, '_' * len(vocabulary))
                else:
                    return text.replace(vocabulary, textReplaceSuccess)
            elif ' ' == list[1][0]:
                textReplaceSuccess = ''
                if ' ' in vocabulary:
                    print(vocabulary)
                    textReplace = vocabulary.split(' ')
                    for idx, itemString in enumerate(textReplace):
                        textReplaceSuccess += itemString.replace(itemString, '_' * len(itemString))
                        if idx < len(textReplace) - 1:
                            textReplaceSuccess += ' '
                if '' == textReplaceSuccess:
                    return text.replace(vocabulary, '_' * len(vocabulary))
                else:
                    return text.replace(vocabulary, textReplaceSuccess)
            else:
                if 'd' == list[1][0]:
                    vocabulary += "d"
                    print(vocabulary)
                    textReplaceSuccess = ''
                    if ' ' in vocabulary:
                        print(vocabulary)
                        textReplace = vocabulary.split(' ')
                        for idx, itemString in enumerate(textReplace):
                            textReplaceSuccess += itemString.replace(itemString, '_' * len(itemString))
                            if idx < len(textReplace) - 1:
                                textReplaceSuccess += ' '
                    if '' == textReplaceSuccess:
                        return text.replace(vocabulary, '_' * len(vocabulary))
                    else:
                        return text.replace(vocabulary, textReplaceSuccess)
                if 's' == list[1][0]:
                    vocabulary += "s"
                    print(vocabulary)
                    textReplaceSuccess = ''
                    if ' ' in vocabulary:
                        print(vocabulary)
                        textReplace = vocabulary.split(' ')
                        for idx, itemString in enumerate(textReplace):
                            textReplaceSuccess += itemString.replace(itemString, '_' * len(itemString))
                            if idx < len(textReplace) - 1:
                                textReplaceSuccess += ' '
                    if '' == textReplaceSuccess:
                        return text.replace(vocabulary, '_' * len(vocabulary))
                    else:
                        return text.replace(vocabulary, textReplaceSuccess)
                elif 'ed' == list[1][:2]:
                    vocabulary += "ed"
                    print(vocabulary)
                    textReplaceSuccess = ''
                    if ' ' in vocabulary:
                        print(vocabulary)
                        textReplace = vocabulary.split(' ')
                        for idx, itemString in enumerate(textReplace):
                            textReplaceSuccess += itemString.replace(itemString, '_' * len(itemString))
                            if idx < len(textReplace) - 1:
                                textReplaceSuccess += ' '
                    if '' == textReplaceSuccess:
                        return text.replace(vocabulary, '_' * len(vocabulary))
                    else:
                        return text.replace(vocabulary, textReplaceSuccess)
                elif 'es' == list[1][:2]:
                    vocabulary += "es"
                    print(vocabulary)
                    textReplaceSuccess = ''
                    if ' ' in vocabulary:
                        print(vocabulary)
                        textReplace = vocabulary.split(' ')
                        for idx, itemString in enumerate(textReplace):
                            textReplaceSuccess += itemString.replace(itemString, '_' * len(itemString))
                            if idx < len(textReplace) - 1:
                                textReplaceSuccess += ' '
                    if '' == textReplaceSuccess:
                        return text.replace(vocabulary, '_' * len(vocabulary))
                    else:
                        return text.replace(vocabulary, textReplaceSuccess)
                elif 'ing' == list[1][:3]:
                    vocabulary += "ing"
                    print(vocabulary)
                    textReplaceSuccess = ''
                    if ' ' in vocabulary:
                        print(vocabulary)
                        textReplace = vocabulary.split(' ')
                        for idx, itemString in enumerate(textReplace):
                            textReplaceSuccess += itemString.replace(itemString, '_' * len(itemString))
                            if idx < len(textReplace) - 1:
                                textReplaceSuccess += ' '
                    if '' == textReplaceSuccess:
                        return text.replace(vocabulary, '_' * len(vocabulary))
                    else:
                        return text.replace(vocabulary, textReplaceSuccess)
                else:
                    textReplaceSuccess = ''
                    if ' ' in vocabulary:
                        print(vocabulary)
                        textReplace = vocabulary.split(' ')
                        for idx, itemString in enumerate(textReplace):
                            textReplaceSuccess += itemString.replace(itemString, '_' * len(itemString))
                            if idx < len(textReplace) - 1:
                                textReplaceSuccess += ' '
                    if '' == textReplaceSuccess:
                        return text.replace(vocabulary, '_' * len(vocabulary))
                    else:
                        return text.replace(vocabulary, textReplaceSuccess)
        else:
            textReplaceSuccess = ''
            if ' ' in vocabulary:
                print(vocabulary)
                textReplace = vocabulary.split(' ')
                for idx, itemString in enumerate(textReplace):
                    textReplaceSuccess += itemString.replace(itemString, '_' * len(itemString))
                    if idx < len(textReplace) - 1:
                        textReplaceSuccess += ' '
            if '' == textReplaceSuccess:
                return text.replace(vocabulary, '_' * len(vocabulary))
            else:
                return text.replace(vocabulary, textReplaceSuccess)
    else:
        print("NoThing")


if __name__ == '__main__':
    # openJson('600WordToiec/Topic.json', True)
    # openJson('600WordToiec/Word.json', False)
    dir = 'Test'

    if not os.path.isdir(dir):
        os.mkdir(dir)
    topic = codecs.open(os.path.join(dir, 'Topic.json'), encoding='utf-8', mode='w')
    word = codecs.open(os.path.join(dir, 'Word.json'), encoding='utf-8', mode='w')

    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM topic")
    topics = cursor.fetchall()

    for item in topics:
        if item['isOpen'] == 1:
            item['isOpen'] = True
        else:
            item['isOpen'] = False

        if item['isLearn'] == 1:
            item['isLearn'] = True
        else:
            item['isLearn'] = False

    cursor.execute(
        "SELECT * FROM word")
    words = cursor.fetchall()

    for item in words:
        if item['isRemember'] == 1:
            item['isRemember'] = True
        else:
            item['isRemember'] = False

        if item['isForgot'] == 1:
            item['isForgot'] = True
        else:
            item['isForgot'] = False

    json.dump(topics, topic, ensure_ascii=False, indent=2)
    json.dump(words, word, ensure_ascii=False, indent=2)
