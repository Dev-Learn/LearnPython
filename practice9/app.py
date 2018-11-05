import bs4
from selenium import webdriver

SOURCE_URL = 'https://blogtruyen.com/danhsach/tatca'
data = []

def main():
    driver = webdriver.Chrome('/usr/local/bin/chromedriver')
    driver.implicitly_wait(30)
    driver.get(SOURCE_URL)
    source = driver.page_source
    getData(source)
    driver.find_element_by_xpath("//a[contains(@href, 'LoadListMangaPage(2)')]").click()
    driver.implicitly_wait(30)
    source = driver.page_source
    getData(source)


def getData(get):
    s = bs4.BeautifulSoup(get, 'lxml')
    items = s.select('div.list > p > span.tiptip.fs-12.ellipsis')
    for item in items:
        link = item.select_one('a')
        link = link.attrs['href'] if link else ''
        data.append(link)


if __name__ == '__main__':
    main()
    print(data)