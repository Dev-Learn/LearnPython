import bs4
import time

import pymysql
import requests
from selenium import webdriver

SOURCE_URL = 'https://blogtruyen.com/theloai/truyen-full'
data = []

# Kết nối vào database.
connection = pymysql.connect(host='localhost',
                             user='root',
                             db='comic',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)


def main():
    driver = webdriver.Chrome('E:/chromedriver_win32/chromedriver.exe')
    driver.implicitly_wait(30)
    driver.get(SOURCE_URL)
    source = driver.page_source
    clickNextPage(source, driver)


# noinspection PyUnreachableCode
def clickNextPage(source, driver):
    page = getData(source)
    print(page)
    if page == '4':
        print('close')
        return
    driver.find_element_by_xpath("//a[contains(@href, 'LoadMangaPage(%s)')]" % str(int(page) + 1)).click()
    driver.implicitly_wait(30)
    time.sleep(2)
    source = driver.page_source
    clickNextPage(source, driver)


def getData(get):
    s = bs4.BeautifulSoup(get, 'lxml')
    page = s.select_one('div.paging > span.current_page').text
    items = s.select('div.list > p > span.tiptip.fs-12.ellipsis')
    for item in items:
        title = item.select_one('a').text
        link = item.select_one('a')
        link = link.attrs['href'] if link else ''
        data.append({'title' : title,'link': link})

    return page


def getComic(data):
    r = requests.get("https://blogtruyen.com/%s" % data['link'])
    # print(r.url)
    comic = {}
    comic['title'] = data['title']
    if r.ok:
        s = bs4.BeautifulSoup(r.content, 'lxml')
        description = s.select_one('div.detail > div.content').text
        comic['description'] = description
        image = s.select_one('div.thumbnail > img')
        image = image.attrs['src'] if image else ''
        comic['image'] = image
        genre = []
        for item in s.select('span.category'):
            genre.append(item.text)
        comic['genre'] = genre
        images = s.select('div.list-wrap > p')
        listImages = []
        for i in range(images.__len__() - 1,-1,-1):
            linkImage = images[i].select_one('a')
            linkImage = linkImage.attrs['href'] if linkImage else ''
            getImagesComic("https://blogtruyen.com/%s" % linkImage, listImages)
        comic['linkImages'] = listImages
    return comic


def getImagesComic(link,listImages):
    r = requests.get(link)
    print(r.url)
    if r.ok:
        s = bs4.BeautifulSoup(r.content, 'lxml')
        items = s.select('article > img')
        for item in items:
            linkImage = item.attrs['src']
            listImages.append(linkImage)


if __name__ == '__main__':
    main()
    if (data):
        # print(data)
        try:
            mycursor = connection.cursor()
            mycursor.execute(
                'CREATE TABLE IF NOT EXISTS linkimage (id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY , idcomic INT ,image VARCHAR(255))')
            mycursor.execute(
                'CREATE TABLE IF NOT EXISTS genre (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, idcomic INT ,genre VARCHAR(255))')
            mycursor.execute(
                'CREATE TABLE IF NOT EXISTS comic (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), description VARCHAR(255),image VARCHAR(255)) DEFAULT CHARSET=utf8')
            for item in data:
                # print('Link : ' + link)
                try:
                    comic = getComic(item)
                    sql = 'INSERT INTO comic (title,description,image) VALUES (%s, %s, %s)'
                    val = (comic['title'], comic['description'],comic['image'])
                    mycursor.execute(sql, val)
                    connection.commit()
                    id = mycursor.lastrowid
                    if id:
                        for item in comic['genre']:
                            sql = 'INSERT INTO genre (idcomic,genre) VALUES (%s, %s)'
                            val = (id, item)
                            mycursor.execute(sql, val)
                            connection.commit()

                        for item in comic['linkImages']:
                            sql = 'INSERT INTO linkimage (idcomic,image) VALUES (%s, %s)'
                            val = (id, item)
                            mycursor.execute(sql, val)
                            connection.commit()
                except Exception as e:
                    print('Error : %s' % str(e))

        finally:
            connection.close()
