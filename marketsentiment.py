from bs4 import BeautifulSoup
import requests
from datetime import date

mytickers = {
    'AAPL':['apple', 'aapl'],
    'TSLA':['tesla', 'tsla'],
    'NVDA':['nvidia', 'nvda'],
    'AMD':['advanced micro devices','amd'],
    'GOOG':['goog', 'alphabet'],
    'FB':['meta', 'facebook', 'fb'],
    'MU':['micron'],
    'MSFT':['microsoft', 'msft'],
    'RBLX':['roblox', 'rblx']
}

today = date.today().strftime('%b. %#d, %Y')
pos_list= ['positive', 'good', 'new ', 'rise', 'rising', 'gains', 'rall', 'jump', 'is up', 'are up', 'was up', 'bull', 'build', 'outperform', 'strong', 'best', 'buy', 'pop', 'win', 'upgrade', 'increas', 'top', 'growth']
neg_list= ['sinks', 'selloff', 'scrutiny', 'fines', 'tumble', 'underperform', 'bad', 'criticism', 'recall', 'drop', 'problem', 'hurdle', 'looms', 'clos', 'anti', 'bear', 'ordered to change', '’t', 'end', 'meme', 'fall', 'downgrade', 'decreas', 'down', 'dip', 'late', 'loss', 'miss']

def check_market_sentiment(stock):
    sentiment_counter = 0
    pos_outlook = 0
    neg_outlook = 0

    post = f"https://www.marketwatch.com/investing/stock/{stock}?mod=quote_search"
    source = requests.get(post).text
    soup = BeautifulSoup(source, 'lxml')
    news  = soup.find_all('div', class_="article__content")
    print(stock) #testing
    for title in news:
        try:
            #sometimes the headline isn't formatting correctly, skip it
            headline = title.h3.a.text.strip().lower()
        except:
            pass

        now = title.div.span.text
        if today in now and any(alternate_names in headline for alternate_names in mytickers[stock]):
            sentiment_counter, pos_outlook, neg_outlook, total, outlook = calculate_article_score(headline, sentiment_counter, pos_outlook, neg_outlook)
            print(total, outlook, headline) #testing

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
    message = f'news is {sentiment}({pos_outlook}|{neg_outlook})'
    return message

# print(check_market_sentiment('AMD')) #test