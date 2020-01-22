import bs4
import requests
from selenium import webdriver

ROOT_LINK1 = "http://www.yeuanhvan.com"
LINK1 = ROOT_LINK1 + "/tips-for-listening-section"
LINK2 = "https://english.best/toeic/"

LISTENING = "Listening"
READING = "Reading"

def main():
    request = requests.get(LINK1)
    if request.ok:
        source = bs4.BeautifulSoup(request.content, 'lxml')
        items = source.select(
            "div.t3-module.module.menu_sidebar > div.module-inner > div.module-ct > ul.nav.nav-pills.nav-stacked.menu > li > a")
        for index, item in enumerate(items):
            if index == items.__len__() - 1:
                continue
            link = item['href']
            getSource(link)


def getSource(link):
    link = ROOT_LINK1 + link
    print(link)
    request = requests.get(link)
    if request.ok:
        source = bs4.BeautifulSoup(request.content, 'lxml')
        items = source.select("table.category.table.table-striped.table-bordered.table-hover > tbody > tr > td > a")
        for item in items:
            text = item.text
            link = item['href']
            if "Part" in text:
                continue

            driver = webdriver.Chrome('D:\chromedriver')
            driver.implicitly_wait(30)
            driver.get(ROOT_LINK1 + link)
            sourceLink = bs4.BeautifulSoup(driver.page_source, 'lxml')
            listTabQuestion = sourceLink.select("ul#set-rl_tabs-1.nav.nav-tabs > li")
            for index, itemQuestion in enumerate(listTabQuestion):
                driver.find_element_by_xpath("""//*[@id="set-rl_tabs-1"]/li[%s]""" % (index + 1)).click()
                driver.implicitly_wait(30)
                sourceCrawl = bs4.BeautifulSoup(driver.page_source, 'lxml')
                image = sourceCrawl.select_one("p.MsoNormal > span > img")['src']
                print(image)


if __name__ == '__main__':
    main()
