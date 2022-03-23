import requests
from time import sleep

s = requests.Session()
s.headers.update({'X-API-key': 'W9OPB2TD'}) # Dektop

MAX_LONG_EXPOSURE = 25000
MAX_SHORT_EXPOSURE = -25000
ORDER_LIMIT = [5000, 1000, 500]
Min_Spread = 0.05
Max_Orders = 5
Bump = .5

def get_tick():
    resp = s.get('http://localhost:9999/v1/case')
    if resp.ok:
        case = resp.json()
        return case['tick'], case['status']

def get_bid_ask(ticker):
    payload = {'ticker': ticker}
    resp = s.get('http://localhost:9999/v1/securities/book', params = payload)
    if resp.ok:
        book = resp.json()
        bid_side_book = book['bids']
        ask_side_book = book['asks']
        
        bid_prices_book = [item["price"] for item in bid_side_book]
        ask_prices_book = [item['price'] for item in ask_side_book]
        
        best_bid_price = bid_prices_book[0]
        best_ask_price = ask_prices_book[0]
  
        return best_bid_price, best_ask_price
    
def get_spread(ticker):
    bid_price, ask_price = get_bid_ask(ticker)
    return (bid_price - ask_price)
    

def get_time_sales(ticker):
    payload = {'ticker': ticker}
    resp = s.get ('http://localhost:9999/v1/securities/tas', params = payload)
    if resp.ok:
        book = resp.json()
        time_sales_book = [item["quantity"] for item in book]
        return time_sales_book

def get_position():
    resp = s.get ('http://localhost:9999/v1/securities')
    if resp.ok:
        book = resp.json()
        return [abs(book[0]['position']) + abs(book[1]['position']) + abs(book[2]['position']),book[0]['position'],book[1]['position'],book[2]['position']]

def get_open_orders(ticker):
    payload = {'ticker': ticker}
    resp = s.get('http://localhost:9999/v1/orders', params = payload)
    if resp.ok:
        orders = resp.json()
        buy_orders = [item for item in orders if item["action"] == "BUY"]
        sell_orders = [item for item in orders if item["action"] == "SELL"]
        return buy_orders, sell_orders

def get_order_status(order_id):
    resp = s.get ('http://localhost:9999/v1/orders' + '/' + str(order_id))
    if resp.ok:
        order = resp.json()
        return order['status']

def buy_sell(sell_price, buy_price, ticker_index, order_num):
    for i in range(order_num):
        
        s.post(('http://localhost:9999/v1/orders', params = {'ticker': ticker, 'type': 'LIMIT', 'quantity': ORDER_LIMIT[ticker_index], 'price': buy_price, 'action': 'BUY'}))
        s.post(('http://localhost:9999/v1/orders', params = {'ticker': ticker, 'type': 'LIMIT', 'quantity': ORDER_LIMIT[ticker_index], 'price': sell_price, 'action': 'SELL'}))
        
        
def open_buys(ticker):
    buy_orders, sells = get_open_orders(ticker)

    open_volume = 0 
    ids = []
    prices = []
    order_volumes = []
    filled_volume = []
    open_orders = buy_orders
        
    for order in open_orders:
        open_volume = open_volume + order['quantity']
        filled_volume.append(order['quantity_filled'])
        order_volumes.append(order['quantity'])
        prices.append(order['price'])
        ids.append(order['order_id'])
    return open_volume, filled_volume, order_volumes, prices, ids

def open_sell(ticker):
    buys, sell_orders = get_open_orders(ticker)

    open_volume = 0 
    ids = []
    prices = []
    order_volumes = []
    filled_volume = []
    open_orders = sell_orders
    tickers = []
        
    for order in open_orders:
        open_volume = open_volume + order['quantity']
        filled_volume.append(order['quantity_filled'])
        order_volumes.append(order['quantity'])
        prices.append(order['price'])
        ids.append(order['order_id'])
        
    return open_volume, filled_volume, order_volumes, prices, ids



def get_open_volume(ticker):
    payload = {'ticker': ticker}
    sell_volume = 0 
    buy_volume = 0
    resp = s.get ('http://localhost:9999/v1/orders', params = payload)
    if resp.ok:
        orders = resp.json()
        buy_orders = [item for item in orders if item["action"] == "BUY"]
        sell_orders = [item for item in orders if item["action"] == "SELL"]
    for orders in sell_orders:
        sell_volume = sell_volume + orders['quantity']
    for orders in buy_orders:
        buy_volume = buy_volume + orders['quantity']
    return buy_volume, sell_volume
    
    
    
    
    
    
    
    
    
def re_order(number_of_orders, ids, volume_filled, volumes, price, action, tickers, ticker_list):
    for i in range(number_of_orders):
        oid = ids[i]
        volume = volumes[i]
        filled = volume_filled[i]
        
        if (volume_filled != 0 ):
            volume = ORDER_LIMIT[ticker_list.index(tickers[i])] - volume_filled
            
            deleted = s.delete('http://localhost:9999/v1/orders/{}'.format(oid))
            if(deleted.ok):
                s.post('http://localhost:9999/v1/orders', params = {'ticker': tickers[i], 'type': 'LIMIT', 'quantity': volume, 'price': price, 'action': action})

def main():
    ticker_list=['CNG','ALG','AC']
    tick, status = get_tick()
    bids = [0,0,0]
    asks = [0,0,0]
    spread = [0,0,0]
    #buy variables 
    buy_ids = [[],[],[]]
    buy_prices = [[],[],[]]
    buy_volumes = [[],[],[]]
    buy_filled_volume = [[],[],[]]
    open_buy_volume = [0,0,0]
    
    #sell variables 
    sell_ids = [[],[],[]]
    sell_prices = [[],[],[]]
    sell_volumes = [[],[],[]]
    sell_filled_volume = [[],[],[]]
    open_sell_volume = [0,0,0]
 
    
    #one-sided-fill variables 
    
    single_side-fill = False
    single_side_trans = 0
    
    while tick > 5 and tick < 295 and not shutdown:
    
        for j in range(3):
        #update status 
            open_sell_volume[j], sell_filled_volume[j], sell_volumes[j], sell_prices[j], sell_ids[j] = open_sell(ticker_list[j])
            open_buy_volume[j], buy_filled_volume[j], buy_volumes[j], buy_prices[j], buy_ids[j]  = open_buys(ticker_list[j])
            
            bids[j], asks[j] = get_bid_ask(ticker_list[j])
            spread[j] = bids[j] - asks[j]
        #order_loops 
        for i in range(3):
            if(open_sell_volume[i] == 0 and open_buy_volume[i] == 0):
                single_side_trans = False
 

if __name__ == '__main__':
    main()



