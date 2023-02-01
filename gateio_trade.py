from decimal import Decimal as D
from re import T
from auth.extract_yaml import *
import time

spot_api = load_gateio_client('auth/auth.yml')


def get_pairs(coin):
        return [(item.id,item.amount_precision) for item in spot_api.list_currency_pairs() if str(item.id).startswith(coin)]

def buy_eth():
    tickers = spot_api.list_tickers(currency_pair = 'ETH_USDT')
    assert len(tickers) == 1
    last_price = float(tickers[0].last)
    accounts = spot_api.list_spot_accounts(currency='USDT')
    assert len(accounts) == 1
    available = D(accounts[0].available)
    order_amount = round(((float(available)/(float(last_price)*1.05)) * 0.99),int(1))
    order = Order(amount = str(order_amount), price = str(float(last_price) * 1.05), side = 'buy', currency_pair = 4)
    #spot_api.create_order(order) #Places the order

#If an appropriate pair exists, places order
def gateio_order(coin):
    not_bought = True
    for coin_pair, precision in get_pairs(coin):
        if str(coin_pair).endswith('_USDT'):
            tickers = spot_api.list_tickers(currency_pair = coin_pair)
            assert len(tickers) == 1
            last_price = float(tickers[0].last)
            if (last_price == 0.0):
                pass
            else:
                accounts = spot_api.list_spot_accounts(currency='USDT')
                assert len(accounts) == 1
                available = D(accounts[0].available)
                order_amount = round(((float(available)/(float(last_price)*1.05)) * 0.99),int(precision))
                buy_order = Order(amount = str(order_amount), price = str(float(last_price) * 1.05), side = 'buy', currency_pair = coin_pair)
                created = spot_api.create_order(buy_order) #Places the buy order
                print("Placed an order on GateIo for the pair: " + coin_pair + " for " + str(order_amount) + " units at a price of " + str(last_price))
                while (created.status == 'open'):
                        pass
                sell_order = Order(amount = str(round(order_amount/2,int(precision))), price = str(float(last_price) * 1.26), side = 'sell', currency_pair = coin_pair)
                spot_api.create_order(sell_order) #Places the sell order
                print("Placed an order on GateIo for the pair: " + coin_pair + " for " + str(order_amount/2) + " units at a price of " + str(last_price*1.26))
                #send_email('Bought on \nGateIo: ' + coin_pair)
                not_bought = False
                break
    if (not_bought):
        for coin_pair, precision in get_pairs(coin):
            if (str(coin_pair).endswith('_ETH')):
                #buy_eth() #Convert USDT to ETH
                #time.sleep(2) #wait 2 secs after bying ETH
                tickers = spot_api.list_tickers(currency_pair = coin_pair)
                assert len(tickers) == 1
                last_price = float(tickers[0].last)
                if (last_price == 0.0):
                   pass
                else:
                    accounts = spot_api.list_spot_accounts(currency='ETH')
                    assert len(accounts) == 1
                    available = D(accounts[0].available)
                    order_amount = round(((float(available)/(float(last_price)*1.05)) * 0.99),int(precision))
                    order = Order(amount = str(order_amount), price = str(float(last_price) * 1.05), side = 'buy', currency_pair = coin_pair)
                    #created = spot_api.create_order(order) #Places the order
                    #send_email('Bought on \nGateIo: ' + coin_pair)
                    while (created.status == 'open'):
                        pass
                    print("Placed an order on GateIo for the pair: " + coin_pair + " for " + str(order_amount) + " units at a price of " + str(last_price))
                    sell_order = Order(amount = str(round(order_amount/2,int(precision))), price = str(float(last_price) * 1.26), side = 'sell', currency_pair = coin_pair)
                    #spot_api.create_order(sell_order) #Places the sell order
                    print("Placed an order on GateIo for the pair: " + coin_pair + " for " + str(order_amount/2) + " units at a price of " + str(last_price*1.26))
                    not_bought = False
                    break

