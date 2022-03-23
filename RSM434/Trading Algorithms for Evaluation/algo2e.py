import requests
from time import sleep

s = requests.Session()
s.headers.update({'X-API-key': 'TGN7XI59'}) # Dektop

MAX_EXPOSURE = 20000
MAX_SHORT_EXPOSURE = -25000
ORDER_LIMIT = [500,500,500]

def get_tick():
    resp = s.get('http://localhost:9999/v1/case')
    if resp.ok:
        case = resp.json()
        return case['tick'], case['status']

def get_bid_ask(ticker):
    payload = {'ticker': ticker}
    resp = s.get ('http://localhost:9999/v1/securities/book', params = payload)
    if resp.ok:
        book = resp.json()
        bid_side_book = book['bids']
        ask_side_book = book['asks']
        
        bid_prices_book = [item["price"] for item in bid_side_book]
        ask_prices_book = [item['price'] for item in ask_side_book]
        
        best_bid_price = bid_prices_book[0]
        best_ask_price = ask_prices_book[0]
  
        return best_bid_price, best_ask_price

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
    resp = s.get ('http://localhost:9999/v1/orders', params = payload)
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

def main():
    tick, status = get_tick()
    ticker_list = ['CNR','ALG','AC']


    while status == 'ACTIVE':        

        for i in range(3,0,-1):

            
            ticker_symbol = ticker_list[i-1]
            #CNR = ticker_list[0]
            #ALG = ticker_list[1]
            #AC = ticker_list[2]
            #flag = 9
            position = get_position()
            #print(position)
            best_bid_price, best_ask_price = get_bid_ask(ticker_symbol)
            
            if position[0] <= MAX_EXPOSURE:
       
                if position[i] < 16000:
                    #print("buy")
                    resp = s.post('http://localhost:9999/v1/orders', params = {'ticker': ticker_symbol, 'type': 'LIMIT', 'quantity': ORDER_LIMIT[i-1], 'price': best_bid_price, 'action': 'BUY'})
              
                if position[i] > -16000:
                    #print("sell")
                    resp = s.post('http://localhost:9999/v1/orders', params = {'ticker': ticker_symbol, 'type': 'LIMIT', 'quantity': ORDER_LIMIT[i-1], 'price': best_ask_price, 'action': 'SELL'})
            if position[i] < -2000:
                resp = s.post('http://localhost:9999/v1/orders', params = {'ticker': ticker_symbol, 'type': 'LIMIT', 'quantity': ORDER_LIMIT[i-1], 'price': best_bid_price, 'action': 'BUY'})
                
            elif position[i] > 2000:
                resp = s.post('http://localhost:9999/v1/orders', params = {'ticker': ticker_symbol, 'type': 'LIMIT', 'quantity': ORDER_LIMIT[i-1], 'price': best_bid_price, 'action': 'SELL'})
                
            
            if i == 1:
                
                sleep(0.3) 

                s.post('http://localhost:9999/v1/commands/cancel', params = {'ticker': ticker_symbol})
            
            #if flag == 9:
                #s.post('http://localhost:9999/v1/commands/cancel', params = {'ticker': ALG})
            #if flag == 7:
                #s.post('http://localhost:9999/v1/commands/cancel', params = {'ticker': AC})
            #if flag == 5:
                #s.post('http://localhost:9999/v1/commands/cancel', params = {'ticker': CNR})
            #if flag == 1:
                #flag = 9
            
            #flag = flag - 1

        tick, status = get_tick()

if __name__ == '__main__':
    main()