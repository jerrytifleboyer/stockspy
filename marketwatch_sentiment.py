from bs4 import BeautifulSoup
import requests
from datetime import date
from config.positive_list import pos_list
from config.negative_list import neg_list
from config.controller import mytickers

today = date.today().strftime('%b. %#d, %Y')

def check_market_sentiment(stock):
    sentiment_counter = 0
    pos_outlook = 0
    neg_outlook = 0

    url = f"https://www.marketwatch.com/investing/stock/{stock}?mod=quote_search"
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    news  = soup.find_all('div', class_="article__content")
    print(stock) #testing
    for title in news:
        try:
            #sometimes their headline isn't formatting correctly
            headline = title.h3.a.text.strip().lower()
            
        except:
            headline = ""

        now = title.div.span.text
        if today in now and any(alternate_names in headline for alternate_names in mytickers[stock]):
            sentiment_counter, pos_outlook, neg_outlook, total, outlook = calculate_article_score(headline, sentiment_counter, pos_outlook, neg_outlook)
            print(total, outlook, headline)

    message = determine_market_sentiment(sentiment_counter, pos_outlook, neg_outlook)
    return message
    
def calculate_article_score(headline, sentiment_counter, pos_outlook, neg_outlook):
    #count pos and neg headlines, regardless of how many overwhelmingly pos or negs are in the sentence
    #each headline only has a weight of 1
    pos_counter = 0
    neg_counter = 0

    for pos in pos_list:
        if pos in headline:
            pos_counter += 1
    for neg in neg_list:
        if neg in headline:
            neg_counter += 1
    total = pos_counter - neg_counter
    if total > 0:
        outlook = "positive"
        pos_outlook += 1
        sentiment_counter +=1
    elif total < 0:
        outlook = "negative"
        neg_outlook += 1
        sentiment_counter -=1
    else:
        outlook = "neutral"
    return sentiment_counter, pos_outlook, neg_outlook, total, outlook

def determine_market_sentiment(sentiment_counter, pos_outlook, neg_outlook):
    if sentiment_counter > 0:
        sentiment = "BULLISH"
    elif sentiment_counter < 0:
        sentiment = "BEARISH"
    else:
        sentiment = "NEUTRAL"
    message = f'{sentiment}({pos_outlook}|{neg_outlook})'
    return message

# print(check_market_sentiment('AMD')) #test