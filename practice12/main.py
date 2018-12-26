import os
import bs4
import requests
import shutil
import json
import codecs
from selenium import webdriver

SOURCE_URL = 'https://www.nhaccuatui.com/bai-hat/top-20.html'
NEW_CHART = 'chart_lw newchart'
UP_CHART = 'chart_lw upchart'
DOWN_CHART = 'chart_lw downchart'
UNCHANGED = 'chart_lw nonechart'

def main():

    driver = webdriver.Chrome('E:/chromedriver_win32/chromedriver.exe')
    driver.implicitly_wait(5)
    driver.get(SOURCE_URL)
    position = 0
    listLink = [SOURCE_URL]
    while position <= 10:
        driver.find_element_by_xpath('//*[@id="prev_foo_video_more"]').click()
        driver.implicitly_wait(5)
        listLink.append(driver.current_url)
        position += 1

    for listChart in listLink:
        r = requests.get(listChart)
        if r.ok:
            s = bs4.BeautifulSoup(r.content, 'lxml')
            week = s.select_one("div.box_view_week > h2").text
            print(week)
            songs = s.select("div.box_resource_slide > ul > li")
            for item in songs:
                song = {}
                position = item.select_one("span").text
                song['position'] = position
                song_name = item.select_one("div.box_info_field > h3 > a")['title']
                song['song_name'] = song_name
                song_link = item.select_one("div.box_info_field > h3 > a")['href']
                song['song_link'] = song_link
                singer = item.select_one("div.box_info_field > h4 > a").text
                song['singer'] = singer
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
                print(song)


if __name__ == '__main__':
    main()