import requests
from bs4 import BeautifulSoup as BS
import re
from coin_check import has_coin
import re
import json

#Checks the binance announcement page for new coin listings.
def check_announcements():
    r = requests.get('https://www.binance.com/en/trade/BTC_USDT?layout=basic')
    html = BS(r.text, 'lxml')

    res = html.find(id = '__APP_DATA')
    json_object = json.loads(res.contents[0])

    news = [str(tradeNews['title']) for tradeNews in json_object['pageData']['redux']['tradeNews']['news'] if (str(tradeNews['title']).startswith('Binance Will List') and (not(str(tradeNews['title']).endswith('the Innovation Zone'))))]

    coins = []

    for annoucement in news:
        res = re.findall(r'\(.*?\)', annoucement)
        for i in res:
            coins.append(i[1:-1])

    if (len(coins) != 0):
        for i in coins:
            print("New coin " + i + " detected!")
            has_coin(i)
        exit()
    else:
        pass #print("No new coin detected")

