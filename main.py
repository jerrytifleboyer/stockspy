#when adding new stocks, update: checkstockprice, checkWSB, marketsentiment
myholdings = {
    'avgAAPLholdings' : 0, #170
    'avgNVDAholdings' : 0, #275
    'avgTSLAholdings' : 0, #920
    'avgAMDholdings' : 150,
    'avgGOOGholdings' : 2905,
    'avgFBholdings' : 339,
    'avgMUholdings' : 95,
    'avgMSFTholdings' : 333,
    'avgRBLXholdings' : 100
}
stocks = "AAPL,NVDA,TSLA,AMD,GOOG,FB,MU,MSFT,RBLX"

import requests
import json
import time
from textme import textme
from checkWSB import check_subreddits
from marketsentiment import check_market_sentiment

with open('config/pw.json') as f:
    data = json.load(f)
    secret = data["FMP_API"]["secret"]

def track_ticker_price(stocks, secret):
    dic = {}
    currprice = 0
    yesterdayClosePrice = 1
    oneBigText = ""
    # vol = 2 #un-used
    # avgVol = 3 #un-used

    #it texts me too much, 30min delay added
    list_of_stocks_moved = []
    timer = 15
    stockAPIdelay = 90
    redditPrawDelay = 5

    print(time.ctime().split(" ")[4])

    while '06:30:00' < time.ctime().split(" ")[4] and time.ctime().split(" ")[4] <'12:30:00': #disable when testing
        if timer == 0: #clear list and restart timer
            list_of_stocks_moved = []
            timer = 15
        elif list_of_stocks_moved: #only decrement the time, if there's a value in the list
            timer -= 1

        tickerdata = requests.get(f'https://financialmodelingprep.com/api/v3/quote/{stocks}?apikey={secret}').json()
        # print(f'directly from the API \n{tickerdata}') #test

        for ii in tickerdata:
            dic[ii['symbol']] = [ii['price'], ii['previousClose'], ii['volume'], ii['avgVolume']]
        print(f'dictionary {dic}')

        for ticker in dic:
            drop2percent = myholdings[f'avg{ticker}holdings'] * 0.975 or dic[ticker][yesterdayClosePrice] * 0.975
            drop5percent = myholdings[f'avg{ticker}holdings'] * 0.95 or dic[ticker][yesterdayClosePrice] * 0.95
            rose5percent = myholdings[f'avg{ticker}holdings'] * 1.05 or dic[ticker][yesterdayClosePrice] * 1.05
            rose2percent = myholdings[f'avg{ticker}holdings'] * 1.025 or dic[ticker][yesterdayClosePrice] * 1.025
            
            oneBigText = report_ticker_movement(ticker, dic[ticker][currprice], drop5percent, drop2percent, rose5percent, rose2percent, list_of_stocks_moved, oneBigText)
            time.sleep(redditPrawDelay)

        if oneBigText:
            textme(oneBigText)
            oneBigText = ""

        time.sleep(stockAPIdelay) #disable when testing

#check stock price, gather return info and text/discord me
def report_ticker_movement(ticker, curr_price, drop5percent, drop2percent, rose5percent, rose2percent, list_of_stocks_moved, oneBigText):
    if ticker not in list_of_stocks_moved:
        #price drops, BUY
        if drop5percent > curr_price:
            movement = f'{ticker} down 5%'
            sentiment = check_market_sentiment(ticker)
            oneBigText += f'{movement}, {sentiment}\n'
            check_subreddits(ticker)
            list_of_stocks_moved.append(ticker)
        elif drop2percent > curr_price:
            movement = f'{ticker} down 2.5%'
            sentiment = check_market_sentiment(ticker)
            check_subreddits(ticker)
            
        #price goes up, SELL
        elif rose5percent < curr_price:
            movement = f'{ticker} up 5%'
            sentiment = check_market_sentiment(ticker)
            oneBigText += f'{movement}, {sentiment}\n'
            check_subreddits(ticker)
            list_of_stocks_moved.append(ticker)
        elif rose2percent < curr_price:
            movement = f'{ticker} up 2.5%'
            sentiment = check_market_sentiment(ticker)
            check_subreddits(ticker)

        return oneBigText

#runs everything below
# textme(f'\r\n{time.ctime()}, good morning cutie-kun')

track_ticker_price(stocks, secret)