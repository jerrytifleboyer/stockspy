#when adding new stocks, update: checkstockprice, checkWSB, marketsentiment
myholdings = {
    'avgAAPLholdings' : 0, #170
    'avgNVDAholdings' : 0, #275
    'avgTSLAholdings' : 0, #920
}
stocks = "AAPL,NVDA,TSLA"

import requests
import json
import time
from textme import textme
from checkWSB import check_subreddits
from marketsentiment import check_market_sentiment

with open('config/pw.json') as f:
    data = json.load(f)
    secret = data["FMP_API"]["secret"]

dic = {}
currprice = 0
openingprice = 1
# vol = 2 #un-used
# avgVol = 3 #un-used

def main(stocks, secret):
    #it texts me too much, 30min buffer time added
    list_of_stocks_moved = []
    timer = 15

    while '06:30:00' < time.ctime().split(" ")[3] and time.ctime().split(" ")[3] <'12:50:00': #disable when testing
        if timer == 0: #clear list and restart timer
            list_of_stocks_moved = []
            timer = 15
        elif list_of_stocks_moved: #only decrement the time, if there's a value in the list
            timer -= 1

        tickerdata = requests.get(f'https://financialmodelingprep.com/api/v3/quote/{stocks}?apikey={secret}').json()
        # print(f'directly from the API \n{tickerdata}') #debug

        for ii in tickerdata:
            dic[ii['symbol']] = [ii['price'], ii['open'], ii['volume'], ii['avgVolume']]
        print(f'dictionary {dic}')

        for ticker in dic:
            drop2percent = myholdings[f'avg{ticker}holdings'] * 0.985 or dic[ticker][openingprice] * 0.975
            drop5percent = myholdings[f'avg{ticker}holdings'] * 0.95 or dic[ticker][openingprice] * 0.95
            rose5percent = myholdings[f'avg{ticker}holdings'] * 1.05 or dic[ticker][openingprice] * 1.05
            rose2percent = myholdings[f'avg{ticker}holdings'] * 1.025 or dic[ticker][openingprice] * 1.025
            check_stock_price(ticker, dic[ticker][currprice], drop5percent, drop2percent, rose5percent, rose2percent, list_of_stocks_moved)

        time.sleep(120) #disable when testing

#check stock price, gather return info and text/discord me
def check_stock_price(ticker, curr_price, drop5percent, drop2percent, rose5percent, rose2percent, list_of_stocks_moved):
    if ticker not in list_of_stocks_moved:
        #price drops, BUY
        if drop5percent > curr_price:
            text = f'{ticker} dropped 5%'
            textme(text)
            check_market_sentiment(ticker)
            check_subreddits(ticker)
        elif drop2percent > curr_price:
            text = f'{ticker} dropped 2.5%'
            textme(text)
            check_market_sentiment(ticker)
            check_subreddits(ticker)
            list_of_stocks_moved.append(ticker)
        #price goes up, SELL
        elif rose5percent < curr_price:
            text = f'{ticker} rose 5%'
            textme(text)
            check_market_sentiment(ticker)
            check_subreddits(ticker)
        elif rose2percent < curr_price:
            text = f'{ticker} rose 2.5%'
            textme(text)
            check_market_sentiment(ticker)
            check_subreddits(ticker)
            list_of_stocks_moved.append(ticker)

#runs everything below
textme(f'\r\n{time.ctime()}, good morning cutie-kun')

main(stocks, secret)