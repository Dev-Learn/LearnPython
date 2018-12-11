import bs4
import time

import pymysql
import requests
from selenium import webdriver
from datetime import datetime, timedelta

SOURCE_URL = 'https://blogtruyen.com/danhsach/tatca'
data = []

# Kết nối vào database.
connection = pymysql.connect(host='localhost',
                             user='root',
                             db='comic',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)


def main():
    driver = webdriver.Chrome('/usr/local/bin/chromedriver')
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
        title = item.select_one('a').text
        link = item.select_one('a')
        link = link.attrs['href'] if link else ''
        data.append({'title': title, 'link': link})

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
        genre = []
        for item in s.select('span.category'):
            genre.append(item.text)
        comic['genre'] = genre
        images = s.select('div.list-wrap > p')
        listImages = []
        for i in range(images.__len__() - 1, -1, -1):
            linkImage = images[i].select_one('a')
            linkImage = linkImage.attrs['href'] if linkImage else ''
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


def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time, datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(second_diff / 60) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(second_diff / 3600) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff / 7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff / 30) + " months ago"
    return str(day_diff / 365) + " years ago"


def updateSQL():
    if data:
        # print(data)
        try:
            mycursor = connection.cursor()
            mycursor.execute(
                'CREATE TABLE IF NOT EXISTS linkimage (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY , idcomic INT ,image VARCHAR(255))')
            mycursor.execute(
                'CREATE TABLE IF NOT EXISTS genre (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, idcomic INT ,genre VARCHAR(255))')
            mycursor.execute(
                'CREATE TABLE IF NOT EXISTS comic (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), description VARCHAR(255)) DEFAULT CHARSET=utf8')
            for item in data:
                # print('Link : ' + link)
                try:
                    comic = getComic(item)
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
                except Exception as e:
                    print('Error : %s' % str(e))

        finally:
            connection.close()


if __name__ == '__main__':
    # main()
    # updateSQL()
    date = datetime.now()
    print(date)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM article")
    articles = cursor.fetchall()
    for item in articles:
        time = item['time_ago']
        if "giờ trước" in time:
            time = date.date()
            print(time)
        elif " ngày trước" in time:
            time = time.split(" ngày trước")
            if "một" in time[0]:
                time = date - timedelta(1)
                print(time.date())
            else:
                time = date - timedelta(int(time[0]))
                print(time.date())
        else:
            time = time.split(" tháng trước")
            if "một" in time[0]:
                time = date - timedelta(1 * 30)
                print(time.date())
            else:
                time = date - timedelta(int(time[0]) * 30)
                print(time.date())
        cursor.execute("UPDATE article SET time_ago = %s where id = %s" % (str(time), item['id']))
        connection.commit()
