import bs4
import time
import requests

import pymysql
from selenium import webdriver

SOURCE_URL = 'https://tinhte.vn/'

# Kết nối vào database.
connection = pymysql.connect(host='localhost',
                             user='root',
                             db='tinhte',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)


def main():
    driver = webdriver.Chrome('E:/chromedriver_win32/chromedriver.exe')
    driver.implicitly_wait(30)
    driver.get(SOURCE_URL)
    position = 0
    source = driver.page_source
    while position < 501:
        driver.find_element_by_xpath('//*[@id="__next"]/div/div[3]/div[1]/div[2]/div/div[2]/button').click()
        driver.implicitly_wait(5)
        source = driver.page_source
        position += 1
        print(position)
    getData(source)


def getData(source):
    mycursor = connection.cursor()
    mycursor.execute(
        'CREATE TABLE article(id int PRIMARY KEY NOT NULL AUTO_INCREMENT,title NVARCHAR(255) NOT NULL,image NVARCHAR(255) NOT NULL,description NVARCHAR(255) NOT NULL,time_ago NVARCHAR(255) NOT NULL,link NVARCHAR(255) NOT NULL)')
    connection.commit()

    s = bs4.BeautifulSoup(source, 'lxml')
    data_source = s.select('ol')[3].select('li')
    for item in data_source:
        article = {}
        link = item.select_one('a')
        link = link.attrs['href'] if link else ''
        article['link'] = link

        title = item.select_one('h3')
        title = title.text if title else ''
        article['title'] = title

        image = item.select_one('img')
        image = image.attrs['src'] if image else ''
        article['image'] = image

        description = item.select('p')
        description = description[0] if description.__len__() > 0 else ''
        description = description.text if description else ''
        article['description'] = description

        time_ago = item.select('span')
        time_ago = time_ago[2] if time_ago.__len__() > 2 else ''
        time_ago = time_ago.text if time_ago else ''
        article['time_ago'] = time_ago
        print(article)

        sql = 'INSERT INTO article (title,image,description,time_ago,link) VALUES (%s, %s, %s, %s, %s)'
        val = (article['title'], article['image'], article['description'], article['time_ago'], article['link'])
        mycursor.execute(sql, val)
        connection.commit()


if __name__ == '__main__':
    # main()

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM article")
    articles = cursor.fetchall()
    for item in articles:
        try:
            r = requests.get(item['link'])
            if r.ok:
                s = bs4.BeautifulSoup(r.content, 'lxml')
                author = s.select_one('div.author > a')
                author_link = author.attrs['href'] if author else ''
                author_name = ''
                author_avarta = ''
                author_image = author.select_one('img')
                author_name = author_image.attrs['alt'] if author_image else ''
                author_avarta = author_image.attrs['src'] if author_image else ''

                cursor.execute("SELECT id FROM author WHERE link = '%s'" % pymysql.escape_string(author_link))
                id = cursor.fetchone()

                if id:
                    cursor.execute("UPDATE article SET id_author = %s WHERE id = %s" % (id['id'], item['id']))
                    connection.commit()
                else:
                    cursor.execute("INSERT author (author_name,avarta,link) VALUES ('%s','%s','%s')" % (
                        author_name, author_avarta, author_link))
                    connection.commit()
                    cursor.execute("SELECT LAST_INSERT_ID()")
                    id_author = cursor.fetchone()
                    cursor.execute(
                        "UPDATE article SET id_author = '%s' WHERE id = %s" % (
                        id_author['LAST_INSERT_ID()'], item['id']))
                    connection.commit()

                detail = s.select('blockquote')
                detail = detail[0] if detail.__len__() > 0 else ''
                detail = detail.text if detail else ''

                cursor.execute("INSERT article_detail (detail) VALUES ('%s')" % pymysql.escape_string(detail.strip()))
                connection.commit()
                cursor.execute("SELECT LAST_INSERT_ID()")

                id_detail = cursor.fetchone()
                cursor.execute("UPDATE article SET id_detail = '%s' WHERE id = %s" % (id_detail['LAST_INSERT_ID()'],item['id']))
                connection.commit()
        except Exception as e:
            print(e)


