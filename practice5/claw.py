from selenium import webdriver
import bs4
import time
import requests

URL = 'https://www.examenglish.com/TOEIC/TOEIC_reading.html'

# install chromedriver
# install ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
# brew tap caskroom/cask
# brew cask install chromedriver
driver = webdriver.Chrome('D:\chromedriver')
driver.implicitly_wait(30)
driver.get(URL)

s = bs4.BeautifulSoup(driver.page_source, 'lxml')
#After opening the url above, Selenium clicks the specific agency link
# driver.find_element_by_id('jplayer_play').click()

# bs4.BeautifulSoup([21].contents[7].text,'html.parser')
# bs4.BeautifulSoup(s.find_all('div')[24].contents[0].text,'lxml')


