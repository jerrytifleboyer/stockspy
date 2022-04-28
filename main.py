import finnhub
import json
import time
from textme import textme
from marketwatch_sentiment import check_market_sentiment
from config.controller import myholdings, stocks

with open('config/pw.json') as f:
    data = json.load(f)
    secret = data['finnhub']['secret']
    finnhub_client = finnhub.Client(api_key=secret)

def track_ticker_price(stocklist):
    movement_tracker = {
        'huge_drops' : '',
        'large_movements' : '',
        'small_movements' : ''
    }
    currprice = 'c'
    yesterdayClosePrice = 'pc'
    
    list_of_stocks_moved = []
    timer = 30
    api_delay = 60
    reddit_delay = 5
    text_delay = 4

    #i think this is the issue, the time from import moves either to position 3/4 thus:
    curr_time = 3 if len(time.ctime().split(' ')[3]) > 4 else 4
    print(time.ctime().split(' ')[curr_time])

    while '06:00:00' < time.ctime().split(' ')[curr_time] < '12:59:00': #disable when testing
        #timer mechanism, limits it from texting me every second
        if timer == 0: 
            list_of_stocks_moved = []
            timer = 20
        elif list_of_stocks_moved: #only decrement the time, if there's a value in the list
            timer -= 1

        for ticker in stocklist:
            #https://finnhub.io/docs/api/quote
            tickerInfo = finnhub_client.quote(ticker)
            drop2percent = myholdings[f'avg{ticker}holdings'] * 0.98 or tickerInfo[yesterdayClosePrice] * 0.98
            drop5percent = myholdings[f'avg{ticker}holdings'] * 0.95 or tickerInfo[yesterdayClosePrice] * 0.95
            drop10percent = myholdings[f'avg{ticker}holdings'] * 0.9 or tickerInfo[yesterdayClosePrice] * 0.9
            rose2percent = myholdings[f'avg{ticker}holdings'] * 1.02 or tickerInfo[yesterdayClosePrice] * 1.02
            rose5percent = myholdings[f'avg{ticker}holdings'] * 1.05 or tickerInfo[yesterdayClosePrice] * 1.05
            report_ticker_movement(ticker, tickerInfo[currprice], tickerInfo[yesterdayClosePrice], drop10percent, drop5percent, drop2percent, rose5percent, rose2percent, list_of_stocks_moved, movement_tracker)
            time.sleep(reddit_delay)

        for key,stocks_moved in movement_tracker.items():
            if stocks_moved:
                textme(stocks_moved)
                movement_tracker.update({key:''})
                time.sleep(text_delay)

        time.sleep(api_delay) #disable when testingf

#check stock price, gather return info and text/discord me
def report_ticker_movement(ticker, curr_price, yest_price, drop10percent, drop5percent, drop2percent, rose5percent, rose2percent, list_of_stocks_moved, movement_tracker):
    my_cost_basis = myholdings[f'avg{ticker}holdings']
    downtrend = f'{round((((my_cost_basis or yest_price) - curr_price)/(my_cost_basis or yest_price))*100,2)}%'
    uptrend = f'{round(((curr_price - my_cost_basis or yest_price)/(my_cost_basis or yest_price))*100,2)}%'

    if ticker not in list_of_stocks_moved:
        #price drops, BUY
        if drop10percent > curr_price:
            movement = f'{ticker}({round(curr_price)}) --{downtrend}'
            sentiment = check_market_sentiment(ticker)
            movement_tracker['huge_drops'] += f'{movement}\n{sentiment}\n'
        elif drop5percent > curr_price:
            movement = f'{ticker}({round(curr_price)}) --{downtrend}'
            sentiment = check_market_sentiment(ticker)
            movement_tracker['large_movements'] += f'{movement}\n{sentiment}\n'
        elif drop2percent > curr_price:
            movement = f'{ticker}({round(curr_price)}) --{downtrend}'
            sentiment = check_market_sentiment(ticker)
            movement_tracker['small_movements'] += f'{movement}\n{sentiment}\n'

        #price goes up, SELL
        elif rose5percent < curr_price:
            movement = f'{ticker}({round(curr_price)}) ++{uptrend}'
            sentiment = check_market_sentiment(ticker)
            movement_tracker['large_movements'] += f'{movement}\n{sentiment}\n'
        elif rose2percent < curr_price:
            movement = f'{ticker}({round(curr_price)}) ++{uptrend}'
            sentiment = check_market_sentiment(ticker)
            movement_tracker['small_movements'] += f'{movement}\n{sentiment}\n'
        list_of_stocks_moved.append(ticker)

track_ticker_price(stocks)