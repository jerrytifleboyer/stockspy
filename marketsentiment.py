from bs4 import BeautifulSoup
import requests
from datetime import date
from textme import textme

mytickers = {
    'AAPL':'apple',
    'TSLA':'tesla',
    'NVDA':'nvidia'
}

today = date.today().strftime('%b. %d, %Y')

neg_list= ['problem', 'hurdle', 'looms', 'clos', 'antitrust', 'bear', 'ordered to change', '’t', 'end', 'meme', 'fall', 'downgrade', 'decreas', 'down', 'dip', 'late', 'loss', 'miss']
pos_list= ['rise', 'gain', 'rall', 'jump', 'is up', 'are up', 'was up', 'bull', 'build', 'outperform', 'strong', 'best', 'buy', 'pop', 'highlight', 'win', 'upgrade', 'increas', 'top', 'growth']

def check_market_sentiment(stock):
        sentiment_counter = 0

        post = f"https://www.marketwatch.com/investing/stock/{stock}?mod=quote_search"
        source = requests.get(post).text
        soup = BeautifulSoup(source, 'lxml')
        news  = soup.find_all('div', class_="article__content")
        for title in news:
            try:
                #sometimes the headline isn't formatting correctly, skip it
                headline = title.h3.a.text.strip().lower()
            except:
                pass

            now = title.div.span.text
            if today in now and mytickers[stock] in headline:
                total, outlook, sentiment_counter = calculate_article_score(headline, sentiment_counter)
                # print(total, outlook, headline)

        determine_market_sentiment(stock, sentiment_counter)

def calculate_article_score(headline, sentiment_counter):
    neg_counter = 0
    pos_counter = 0

    for neg in neg_list:
        if neg in headline:
            neg_counter += 1
    for pos in pos_list:
        if pos in headline:
            pos_counter += 1
    total = pos_counter - neg_counter
    if total > 0:
        outlook = "positive"
        sentiment_counter +=1
    elif total < 0:
        outlook = "negative"
        sentiment_counter -=1
    else:
        outlook = "neutral"
    return total, outlook, sentiment_counter

def determine_market_sentiment(stock, sentiment_counter):
    if sentiment_counter > 0:
        sentiment = "BULLISH"
    elif sentiment_counter < 0:
        sentiment = "BEARISH"
    else:
        sentiment = "KANGAROO-ISH"
    message = f'{stock} news is {sentiment}({sentiment_counter}) today'
    # print(message)
    textme(message)

# check_market_sentiment('TSLA') #test