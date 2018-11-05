import bs4
import time

import pymysql
import requests
from selenium import webdriver

SOURCE_URL = 'https://blogtruyen.com/danhsach/tatca'
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
    if page == '11':
        print('close')
        return
    driver.find_element_by_xpath("//a[contains(@href, 'LoadListMangaPage(%s)')]" % str(int(page) + 1)).click()
    driver.implicitly_wait(30)
    time.sleep(2)
    source = driver.page_source
    clickNextPage(source, driver)


def getData(get):
    s = bs4.BeautifulSoup(get, 'lxml')
    page = s.select_one('div.paging > span.current_page').text
    items = s.select('div.list > p > span.tiptip.fs-12.ellipsis')
    for item in items:
        link = item.select_one('a')
        link = link.attrs['href'] if link else ''
        data.append(link)

    return page


def getComic(link):
    r = requests.get(link)
    # print(r.url)
    comic = {}
    if r.ok:
        s = bs4.BeautifulSoup(r.content, 'lxml')
        title = s.select_one('h1.entry-title').text
        comic['title'] = title
        description = s.select_one('div.detail > div.content').text
        comic['description'] = description
        genre = []
        for item in s.select('span.category'):
            genre.append(item.text)
        comic['genre'] = genre
        images = s.select('div.list-wrap > p')
        listImages = []
        for i in range(images.__len__() - 1,-1,-1):
            linkImage = images[i].select_one('a')
            linkImage = linkImage.attrs['href'] if link else ''
            listImages.append(getImagesComic("https://blogtruyen.com/%s" % linkImage))
        comic['linkImages'] = listImages
    return comic


def getImagesComic(link):
    r = requests.get(link)
    print(r.url)
    linkImages = []
    if r.ok:
        s = bs4.BeautifulSoup(r.content, 'lxml')
        items = s.select('article')
        for item in items:
            linkImage = item.select_one('img')
            linkImage = linkImage.attrs['src'] if linkImage else ''
            linkImages.append(linkImage)
    return linkImages


if __name__ == '__main__':
    main()
    if (data):
        # print(data)
        try:
            mycursor = connection.cursor()
            mycursor.execute(
                'CREATE TABLE IF NOT EXISTS linkimage (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY , idcomic INT ,image VARCHAR(255))')
            mycursor.execute(
                'CREATE TABLE IF NOT EXISTS genre (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, idcomic INT ,genre VARCHAR(255))')
            mycursor.execute(
                'CREATE TABLE IF NOT EXISTS comic (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), description VARCHAR(255))')
            for link in data:
                # print('Link : ' + link)
                comic = getComic("https://blogtruyen.com/%s" % link)
                sql = 'INSERT INTO comic (title,description) VALUES (%s, %s)'
                val = (comic['title'], comic['description'])
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

        finally:
            connection.close()
