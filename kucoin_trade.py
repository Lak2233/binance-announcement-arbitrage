from auth.extract_yaml import *

client = load_kukoin_client('auth/auth.yml')

#gets the available funds of the given currency
def get_avail_balance(currency):
    for account in client.get_accounts():
        if account['currency'] == currency:
            return account['balance']

def get_pairs(coin):
        return [(symbol['symbol'], int((len(str(symbol['priceIncrement'])) - 2))) for symbol in client.get_symbols() if str(symbol['symbol']).startswith(coin)]

#If an appropriate pair exists, places order
def kucoin_order(coin):
    not_bought = True
    for pair,val in get_pairs(coin):
        if str(pair).endswith('-USDT'):
            client.create_market_order(pair, KuClient.SIDE_BUY, funds = str(round(float(get_avail_balance('USDT')) * 0.99,val)))
            send_email('Bought on \nKucoin: ' + pair)
            print("Placed an order on KuCoin for the pair: " + pair)
            not_bought = False
            break
    for pair,val in get_pairs(coin):
        if str(pair).endswith('-BTC') and not_bought:
            #If USDT pair doesnt exist, convert all availabve USDT to BTC and buy the BTC pair.
            client.create_market_order('BTC-USDT', KuClient.SIDE_BUY, funds = str(round(float(get_avail_balance('USDT')) * 0.99,1)))
            #time.sleep(2) #wait 2 secs after bying btc
            client.create_market_order('pair', KuClient.SIDE_BUY, funds = str(round(float(get_avail_balance('BTC')) * 0.99,val)))
            print("Placed an order on KuCoin for the pair: " + pair)
            break