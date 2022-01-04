from bs4 import BeautifulSoup
import requests
from datetime import date

mytickers = {
    'AAPL':'apple',
    'TSLA':'tesla',
    'NVDA':'nvidia',
    'AMD':'amd',
    'GOOG':'google',
    'FB':'meta',
    'MU':'micron',
    'MSFT':'microsoft',
    'RBLX':'roblox'
}

today = date.today().strftime('%b. %#d, %Y')
# print(today) #testing purposes
neg_list= ['bad', 'criticism', 'recall', 'drop', 'problem', 'hurdle', 'looms', 'clos', 'antitrust', 'bear', 'ordered to change', '’t', 'end', 'meme', 'fall', 'downgrade', 'decreas', 'down', 'dip', 'late', 'loss', 'miss']
pos_list= ['good', 'new', 'rise', 'gain', 'rall', 'jump', 'is up', 'are up', 'was up', 'bull', 'build', 'outperform', 'strong', 'best', 'buy', 'pop', 'win', 'upgrade', 'increas', 'top', 'growth']

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
                sentiment_counter, pos_counter, neg_counter, total, outlook = calculate_article_score(headline, sentiment_counter)
                # print(total, outlook, headline) #testing

        message = determine_market_sentiment(stock, sentiment_counter, pos_counter, neg_counter)
        return message

def calculate_article_score(headline, sentiment_counter):
    #count pos and neg headlines, regardless of how many overwhelmingly pos or negs are in the sentence
    #each headline only has a weight of 1
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
    return sentiment_counter, pos_counter, neg_counter, total, outlook

def determine_market_sentiment(stock, sentiment_counter, pos_counter, neg_counter):
    if sentiment_counter > 0:
        sentiment = "BULLISH"
    elif sentiment_counter < 0:
        sentiment = "BEARISH"
    else:
        sentiment = "KANGAROO-ISH"
    message = f'{stock} news is {sentiment}({pos_counter})|({neg_counter}) today'
    return message

# print(check_market_sentiment('TSLA')) #test