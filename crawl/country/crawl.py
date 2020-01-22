import os
import bs4
import requests
import shutil
import json
import codecs
import cv2

SOURCE_URL = 'http://www.lingoes.net/en/translator/langcode.htm'

def main():
    r = requests.get(SOURCE_URL)
    if r.ok:
        s = bs4.BeautifulSoup(r.content, 'lxml')
        table = s.find('table')
        rows = table.find_all('tr')
        data = []
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])  # Get rid of empty values'
        print(data)
        list = []
        for item in data:
            try:
                language_code = str(item[0]).strip().lower()
                name = str(item[1]).strip()
                print(language_code)
                print(name)
        #         iso_code = str(item[2]).split(" / ")[0].strip().lower()
        #         population = str(item[3]).strip().lower()
        #         area = str(item[4]).strip().lower()
        #         gdp = str(item[5]).strip().lower()
        #         list.append(
        #             {"COUNTRY": name, "COUNTRY CODE": country_code, "ISO CODES": iso_code, "POPULATION": population,
        #              "AREA KM2": area, "GDP $USD": gdp})
                if "-" not in language_code:
                    list.append({"Language_Code" : language_code,"Name" : name})
            except Exception as e:
                print(e)
        print(list)
        countries = codecs.open('Language_Country.json', encoding='utf-8', mode='w')
        json.dump(list, countries, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()
