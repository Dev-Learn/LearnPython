import requests

"""
    flask run --help

    Chương trình lay gia bitcon USD tu API
"""

URL = 'https://api.coindesk.com/v1/bpi/currentprice/USD.json'

def getBTC():
    api = requests.get(URL)
    if api.ok:
        data = api.json()
        btc_data = data['bpi']['USD']['rate']
        return btc_data
    else:
        return 'Không truy cập được !!!'

if __name__ == '__main__':
    print(getBTC())