from kucoin_trade import client, kucoin_order
from gate_api import ApiClient, Configuration, SpotApi
from gateio_trade import gateio_order
import requests

kucoin =  [currencies['currency'] for currencies in client.get_currencies()]

kraken = [key for key in (requests.get('https://api.kraken.com/0/public/Assets').json())['result'].keys()]

#bittrex = [coin['Currency'] for coin in (requests.get('https://api.bittrex.com/api/v1.1/public/getcurrencies').json())['result']]
#bittrex_pairs = [(coin['MarketCurrency'] + coin['BaseCurrency']) for coin in (requests.get('https://api.bittrex.com/api/v1.1/public/getmarkets').json())['result']]

gateio = [x.base for x in (SpotApi(ApiClient(Configuration(key = "", secret = ""))).list_currency_pairs())]


#Checks the exchanges KuCoin, Kraken, BitTrex and GateIO to see if they have the coin of interest already listed.
def has_coin(coin):
    for i in kucoin:
        if str(i).startswith(coin):
            print(coin + " is in KuCoin!")
            kucoin_order(coin)
            pass
    if (coin in kraken):
        print(coin + " is in Kraken!")
        pass
    #if (coin in bittrex):
        #print(coin + " is in BitTrex!")
        #pass
    if (coin in gateio):
        print(coin + " is in GateIo!")
        gateio_order(coin)
        pass
    else:
        pass
