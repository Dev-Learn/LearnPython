import bs4
import requests
from selenium import webdriver

ROOT_LINK1 = "http://www.yeuanhvan.com"
LINK_LISTENING_PART_1 = ROOT_LINK1 + "/part-1-photographs"
LINK_LISTENING_PART_2 = ROOT_LINK1 + "/part-2-questions-responses"
ROOT_LINK2 = "https://english.best/toeic/"

LISTENING = "Listening"
READING = "Reading"


def main():
    request = requests.get(LINK_LISTENING_PART_1)
    if request.ok:
        source = bs4.BeautifulSoup(request.content, 'lxml')
        items = source.select("tbody > tr")
        for index, item in enumerate(items):
            crawlData(item.select_one("a")['href'])
            break


def crawlData(link):
    print(link)
    driver = webdriver.Chrome('E:\chromedriver_win32\chromedriver')
    driver.implicitly_wait(30)
    driver.get(ROOT_LINK1 + link)
    sourceLink = bs4.BeautifulSoup(driver.page_source, 'lxml')
    listTabQuestion = sourceLink.select("ul#set-rl_tabs-1 > li")
    for index, itemQuestion in enumerate(listTabQuestion):
        driver.find_element_by_xpath("""//*[@id="set-rl_tabs-1"]/li[%s]""" % (index + 1)).click()
        driver.implicitly_wait(30)
        sourceCrawl = bs4.BeautifulSoup(driver.page_source, 'lxml')
        sourceCrawl = sourceCrawl.select_one("div.tab-pane.rl_tabs-pane.nn_tabs-pane.active")
        contentImages = sourceCrawl.select("p")
        for contentImage in contentImages:
            if contentImage.find('img'):
                image = contentImage.select_one('img')['src']
                print(image)
                break
        audio = sourceCrawl.select_one("audio")['src']
        print(audio)
        driver.find_element_by_xpath("""//*[@id="set-rl_sliders-%s"]/div[1]""" % (index + 1)).click()
        driver.implicitly_wait(30)
        sourceCrawl = bs4.BeautifulSoup(driver.page_source, 'lxml')
        answerCorrectContents = sourceCrawl.select_one("div.tab-pane.rl_tabs-pane.nn_tabs-pane.active").select_one(
            "div.accordion-inner.panel-body").select('td')
        for indexAnswer, answerCorrectContent in enumerate(answerCorrectContents):
            if "rgb(255, 255, 153)" in str(answerCorrectContent):
                print(indexAnswer)
                break

        driver.find_element_by_xpath("""//*[@id="set-rl_sliders-%s"]/div[2]""" % (index + 1)).click()
        driver.implicitly_wait(30)
        sourceCrawl = bs4.BeautifulSoup(driver.page_source, 'lxml')
        answerContents = sourceCrawl.select_one("div.tab-pane.rl_tabs-pane.nn_tabs-pane.active").select(
            "div.accordion-inner.panel-body")[1].select('span')
        for indexAnswer, answerContent in enumerate(answerContents):
            if "(A)" in str(answerContent):
                answers = answerContent.text.split("\n")
                print(answers)
                break


if __name__ == '__main__':
    main()
