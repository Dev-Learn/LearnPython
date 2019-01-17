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
        if isTopic:
            try:
                mycursor = connection.cursor()
                mycursor.execute(
                    'CREATE TABLE IF NOT EXISTS topic (id INT PRIMARY KEY, topic_en VARCHAR(255), topic_vi VARCHAR(255), image VARCHAR(255))')
                for item in data:
                    sql = 'INSERT INTO topic (id, topic_en,topic_vi,image) VALUES (%s, %s, %s, %s)'
                    val = (item['id'], item['topic_en'], item['topic_vi'], item['image'])
                    mycursor.execute(sql, val)
                    connection.commit()
            finally:
                connection.close()
        else:
            try:
                mycursor = connection.cursor()
                mycursor.execute(
                    """CREATE TABLE IF NOT EXISTS word (id INT PRIMARY KEY, id_topic INT ,vocabulary VARCHAR(255),spelling VARCHAR(255)
                    ,from_type VARCHAR(255),explain_vi VARCHAR(255),explain_en VARCHAR(255),example_en VARCHAR(255),example_vi VARCHAR(255)
                    ,image VARCHAR(255),audio VARCHAR(255))""")
                for item in data:
                    sql = """INSERT INTO word (id, id_topic,vocabulary,spelling,from_type,explain_vi,explain_en,example_en,example_vi,image,audio) 
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                    val = (item['id'], item['id_topic'], item['vocabulary'], item['spelling'], item['from_type'],
                           item['explain_vi']
                           , item['explain_en'], item['example_en'], item['example_vi'], item['image'], item['audio'])
                    mycursor.execute(sql, val)
                    connection.commit()
            finally:
                connection.close()


if __name__ == '__main__':
    openJson('600WordToiec/Topic.json', True)
    openJson('600WordToiec/Word.json', False)
#