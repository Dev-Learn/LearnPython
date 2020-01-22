import os
import bs4
import pymysql
import requests
import json
from selenium import webdriver

SOURCE_URL = 'https://www.nhaccuatui.com/bai-hat/top-20.html'
NEW_CHART = 'chart_lw newchart'
UP_CHART = 'chart_lw upchart'
DOWN_CHART = 'chart_lw downchart'
UNCHANGED = 'chart_lw nonechart'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


def conn():
    return pymysql.connect(host='localhost',
                           user='root',
                           db='chart_song',
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)


# create table singer
# (
#   id   int auto_increment
#     primary key,
#   name varchar(255) charset utf8 not null
# );
#
# create table singer_song
# (
#   id_song   bigint not null,
#   id_singer int    not null,
#   primary key (id_song, id_singer)
# );
#
# create table song
# (
#   id         bigint auto_increment
#     primary key,
#   name       varchar(255) charset utf8 not null,
#   image      varchar(255) charset utf8 not null,
#   link128    varchar(255) charset utf8 null,
#   link320    varchar(255) charset utf8 null,
#   lossless   varchar(255) charset utf8 null,
#   link_local varchar(255) charset utf8 null
# );
#
# create table week
# (
#   id   int auto_increment
#     primary key,
#   name varchar(255) not null
# );
#
# create table week_song
# (
#   id_week             int    not null,
#   id_song             bigint not null,
#   position            int    null,
#   hierarchical        int    null,
#   hierarchical_number int    null,
#   primary key (id_week, id_song)
# );


def main():
    driver = webdriver.Chrome('D:\chromedriver')
    driver.implicitly_wait(5)
    driver.get(SOURCE_URL)
    position = 0
    listLink = [SOURCE_URL]
    while position <= 20:
        driver.find_element_by_xpath('//*[@id="prev_foo_video_more"]').click()
        driver.implicitly_wait(5)
        listLink.append(driver.current_url)
        position += 1

    for listChart in listLink:
        print(listChart)
        r = requests.get(listChart)
        if r.ok:
            s = bs4.BeautifulSoup(r.content, 'lxml')
            week = s.select_one("div.box_view_week > h2").text
            print(week)
            songs = s.select("div.box_resource_slide > ul > li")
            for item in songs:
                song = {'week': week}
                position = item.select_one("span").text
                song['position'] = position
                song_image = item.select_one("div.box_info_field > a > img")['src']
                song['song_image'] = song_image
                song_name = item.select_one("div.box_info_field > h3 > a").text
                song['song_name'] = song_name
                song_link = item.select_one("div.box_info_field > h3 > a")['href']
                song['song_link'] = song_link
                singer = item.select_one("div.box_info_field > h4 > a").text
                song['singer'] = singer
                print(singer)
                chart = item.select("span")[1]
                hierarchical_number = None
                if UP_CHART in str(chart):
                    hierarchical = 1
                    hierarchical_number = chart.text.strip()
                elif DOWN_CHART in str(chart):
                    hierarchical = 2
                    hierarchical_number = chart.text.strip()
                elif NEW_CHART in str(chart):
                    hierarchical = 3
                else:
                    hierarchical = 4
                song['hierarchical'] = hierarchical
                song['hierarchical_number'] = hierarchical_number

                getLinkSong(song)
                insertDB(song)


def getLinkSong(song):
    try:
        id = song['song_link'].split('.')[3]
        url = 'https://graph.nhaccuatui.com/v1/commons/token'
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Host': 'graph.nhaccuatui.com',
                   'Connection': 'Keep-Alive'}

        payload = {'deviceinfo': '{"DeviceID":"dd03852ada21ec149103d02f76eb0a04","DeviceName":"AppTroLyBeDieu", \
            "OsName":"WINDOWS","OsVersion":"8.0","AppName":"NCTTablet","AppTroLyBeDieu":"1.3.0", \
            "UserName":"0","QualityPlay":"128","QualityDownload":"128","QualityCloud":"128","Network":"WIFI","Provider":"NCTCorp"}', \
                   'md5': 'ebd547335f855f3e4f7136f92ccc6955', 'timestamp': '1499177482892'}
        r = requests.post(url, data=payload, headers=headers)
        decoded = json.loads(r.text)
        token = decoded['data']['accessToken']
        gurl = 'https://graph.nhaccuatui.com/v1/songs/' + id + '?access_token=' + token
        content = requests.get(gurl)
        result = json.loads(content.text)
        link128 = result['data']['11']
        link320 = result['data']['12']
        lossless = result['data']['19']
        song['link128'] = link128
        song['link320'] = link320
        song['lossless'] = lossless
        download(song)
        return True
    except Exception as e:
        print(e)
    return False


def download(song):
    target = os.path.join(APP_ROOT, 'songs')
    print(target)

    filename = song['song_name']

    if not os.path.isdir(target):
        os.mkdir(target)

    destination = '/'.join([target, filename + ".mp3"])

    r = requests.get(song['lossless'])

    print(r.status_code)
    if r.status_code == 200:
        with open(destination, 'wb') as f:
            f.write(r.content)
        song['local_link'] = destination
    else:
        song['local_link'] = None


def insertDB(song):
    connection = conn()
    cursor = connection.cursor()
    try:
        week = song['week']
        cursor.execute("select `id` FROM `week` where `name` = '%s'" % week)
        id_week = cursor.fetchone()
        if not id_week:
            sql = "INSERT INTO `week` (name) VALUES (%s)"
            val = week
            cursor.execute(sql, val)
            id_week = cursor.lastrowid
        else:
            id_week = id_week['id']
        cursor.execute("Select `id` From `song` where `name` = '%s'" % song['song_name'])
        idSong = cursor.fetchone()
        if not idSong:
            sql = "INSERT INTO `song` (name,image,link128,link320,lossless,link_local) VALUES (%s,%s,%s,%s,%s,%s)"
            val = (song['song_name'], song['song_image'], song['link128'], song['link320'], song['lossless'],
                   song['local_link'])
            cursor.execute(sql, val)
            idSong = cursor.lastrowid
        else:
            idSong = idSong['id']
        sql = "INSERT INTO `week_song` (id_week,id_song,position,hierarchical,hierarchical_number) VALUES (%s,%s,%s,%s,%s)"
        val = (id_week, idSong, song['position'], song['hierarchical'], song['hierarchical_number'])
        cursor.execute(sql, val)

        singer = song['singer']
        if ', ' in singer:
            singers = singer.split(', ')
            for singer in singers:
                insertSingerSong(cursor, singer, idSong)
        else:
            insertSingerSong(cursor, singer, idSong)
        connection.commit()
    except Exception as e:
        return print(e)
    finally:
        connection.close()
        cursor.close()


def insertSingerSong(cursor, singer, idsong):
    cursor.execute("select `id` FROM `singer` where `name` = '%s'" % singer)
    id = cursor.fetchone()
    if id:
        idSinger = id['id']
        sql = "INSERT INTO `singer_song` (id_song,id_singer) VALUES (%s,%s)"
        val = (idsong, idSinger)
        cursor.execute(sql, val)
    else:
        sql = "INSERT INTO `singer` (name) VALUES (%s)"
        val = singer
        cursor.execute(sql, val)
        idSinger = cursor.lastrowid
        sql = "INSERT INTO `singer_song` (id_song,id_singer) VALUES (%s,%s)"
        val = (idsong, idSinger)
        cursor.execute(sql, val)


if __name__ == '__main__':
    # createTable()
    main()
