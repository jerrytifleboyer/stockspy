myholdings = {
    'avgAAPLholdings' : 0, #170
    'avgNVDAholdings' : 0, #275
    'avgTSLAholdings' : 10, #920
}

import requests
import json
import time
from textme import textme
from checkWSB import checkout_subreddit
from discord import ping_me_on_discord

with open('config/pw.json') as f:
    data = json.load(f)
    secret = data["FMP_API"]["secret"]

dic = {}
currprice = 0
openingprice = 1
movingavg = 2 #the moving average is an array size of 2
vol = 3
avgVol = 4

#it texts me too much, 30min buffer time added
dropping = []
rising = []
timer = 10

#fills up my dictionary in the first run, so i have data to work with
def setup():
    textme(f'{time.ctime()}, i am on!')
    data = requests.get(f'https://financialmodelingprep.com/api/v3/quote/AAPL,NVDA,TSLA?apikey={secret}').json()
    # print(data)
    for ii in data:
        dic[ii['symbol']] = [ii['price'], ii['open'], [ii['open']]*2, ii['volume'], ii['avgVolume']]
setup()

#check stock price, gather return info and text/discord me
def checkstockprice(ticker, curr_price, moving_avg, drop5percent, drop2percent, rose5percent, rose2percent):
    moving_avg.pop(0)
    moving_avg.append(curr_price)
    moving_avg = sum(moving_avg)/2 #the moving average is an array size of 2
    #TODO, do something with moving averages, trending downward/upward?
    #TODO, do something with volume?
    print(ticker)
    if ticker not in dropping and rising:
        #price drops, BUY
        if drop5percent > curr_price:
            text = f'{ticker} dropped 5%'
            dropping.append(ticker)
            textme(text)
            checkout_subreddit(ticker)
        elif drop2percent > curr_price:
            text = f'{ticker} dropped 2.5%'
            dropping.append(ticker)
            textme(text)

        #price goes up, SELL
        elif rose5percent < curr_price:
            text = f'{ticker} rose 5%'
            rising.append(ticker)
            textme(text)
            checkout_subreddit(ticker)
        elif rose2percent < curr_price:
            pass
        #idk what to do, prob nothing cause who cares if it goes up 2.5%

    # time.sleep(60)

# while '06:00:00' < time.ctime().split(" ")[3] and time.ctime().split(" ")[3] <'12:50:00':
if timer == 0:
    dropping = []
    rising = []
    timer = 10
timer-=1

data = requests.get(f'https://financialmodelingprep.com/api/v3/quote/AAPL,NVDA,TSLA?apikey={secret}').json()
for ticker in dic:
    drop2percent = myholdings[f'avg{ticker}holdings'] * 0.985 or dic[ticker][openingprice] * 0.985
    drop5percent = myholdings[f'avg{ticker}holdings'] * 0.95 or dic[ticker][openingprice] * 0.95
    rose5percent = myholdings[f'avg{ticker}holdings'] * 1.05 or dic[ticker][openingprice] * 1.05
    rose2percent = myholdings[f'avg{ticker}holdings'] * 1.025 or dic[ticker][openingprice] * 1.025
    checkstockprice(ticker, dic[ticker][currprice], dic[ticker][movingavg], drop5percent, drop2percent, rose5percent, rose2percent)