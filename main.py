#when adding new stocks, update: checkstockprice, checkWSB, marketsentiment
myholdings = {
    'avgAAPLholdings' : 0, #170
    'avgNVDAholdings' : 0, #275
    'avgTSLAholdings' : 0, #920
    'avgAMDholdings' : 150,
    'avgGOOGholdings' : 2905,
    'avgFBholdings' : 339,
    'avgMUholdings' : 95,
    'avgMSFTholdings' : 328,
    'avgRBLXholdings' : 100
}
stocks = ["AAPL","NVDA","TSLA","AMD","GOOG","FB","MU","MSFT","RBLX"]

import finnhub
import json
import time
from textme import textme
from checkWSB import check_subreddits
from marketsentiment import check_market_sentiment

with open('config/pw.json') as f:
    data = json.load(f)
    secret = data["finnhub"]["secret"]
    finnhub_client = finnhub.Client(api_key=secret)

def track_ticker_price(stocklist):
    currprice = "c"
    yesterdayClosePrice = "pc"
    oneBigText = ""
    
    list_of_stocks_moved = []
    timer = 30
    stockAPIdelay = 60
    redditPrawDelay = 5

    #i think this is the issue, the time from import moves either to position 3/4 thus:
    curr_time = 3 if len(time.ctime().split(" ")[3]) > 4 else 4
    print(time.ctime().split(" ")[curr_time])

    while '06:30:00' < time.ctime().split(" ")[curr_time] < '12:30:00': #disable when testing
    #timer mechanism, limits it from texting me every second
        if timer == 0: 
            list_of_stocks_moved = []
            timer = 30
        elif list_of_stocks_moved: #only decrement the time, if there's a value in the list
            timer -= 1

        for ticker in stocklist:
            tickerInfo = finnhub_client.quote(ticker)
            drop2percent = myholdings[f'avg{ticker}holdings'] * 0.975 or tickerInfo[yesterdayClosePrice] * 0.975
            drop5percent = myholdings[f'avg{ticker}holdings'] * 0.95 or tickerInfo[yesterdayClosePrice] * 0.95
            rose5percent = myholdings[f'avg{ticker}holdings'] * 1.05 or tickerInfo[yesterdayClosePrice] * 1.05
            rose2percent = myholdings[f'avg{ticker}holdings'] * 1.025 or tickerInfo[yesterdayClosePrice] * 1.025
            oneBigText = report_ticker_movement(ticker, tickerInfo[currprice], tickerInfo[yesterdayClosePrice], drop5percent, drop2percent, rose5percent, rose2percent, list_of_stocks_moved, oneBigText)
            time.sleep(redditPrawDelay)

        if oneBigText:
            textme(oneBigText)
            oneBigText = ""

        time.sleep(stockAPIdelay) #disable when testing

#check stock price, gather return info and text/discord me
def report_ticker_movement(ticker, curr_price, yest_price, drop5percent, drop2percent, rose5percent, rose2percent, list_of_stocks_moved, oneBigText):
    up = "\U0001F4C8"
    down = "\U0001F4C9"
    my_cost_basis = myholdings[f'avg{ticker}holdings']
    downtrend = f'{round((((my_cost_basis or yest_price)-curr_price)/(my_cost_basis or yest_price))*100,2)}%'
    uptrend = f'{round(((curr_price-my_cost_basis or yest_price)/(my_cost_basis or yest_price))*100,2)}%'

    if ticker not in list_of_stocks_moved:
        #price drops, BUY
        if drop5percent > curr_price:
            movement = f'{ticker}({round(curr_price)}) down {downtrend}'
            sentiment = check_market_sentiment(ticker)
            oneBigText += f'{movement}, {sentiment}\n'
            check_subreddits(ticker)
            list_of_stocks_moved.append(ticker)
        elif drop2percent > curr_price:
            movement = f'{ticker}({round(curr_price)}) down {downtrend}'
            textme(movement)
            list_of_stocks_moved.append(ticker)

        #price goes up, SELL
        elif rose5percent < curr_price:
            movement = f'{ticker}({round(curr_price)}) up {uptrend}'
            sentiment = check_market_sentiment(ticker)
            oneBigText += f'{movement}, {sentiment}\n'
            check_subreddits(ticker)
            list_of_stocks_moved.append(ticker)
        elif rose2percent < curr_price:
            movement = f'{ticker}({round(curr_price)}) up {uptrend}'
            textme(movement)
            list_of_stocks_moved.append(ticker)
    return oneBigText

track_ticker_price(stocks)