# reddit acc info from:  https://www.reddit.com/prefs/apps 
import json
import praw #this works, it's lying

mytickers = {
    'AAPL':'APPLE',
    'TSLA':'TESLA',
    'NVDA':'NVIDIA'
}

subredditlist = ['wallstreetbets', 'stocks', 'investing', 'stockmarket']

ignored_keywords = ['gallery', 'redd.it']

# ticker = "TSLA" #test

def create_reddit_object():
    with open('config/pw.json') as f:
        data = json.load(f)
        reddit = praw.Reddit(
            client_id=data['reddit']['account'], 
            client_secret=data['reddit']['secret'], 
            user_agent=data['reddit']['alias'])
    return reddit
reddit = create_reddit_object()

def checkout_subreddit(ticker):
    headlines = {}
    keyword = [ticker, mytickers[ticker]]
    for subreddit in subredditlist:
        for submission in reddit.subreddit(subreddit).new(limit=100):
            if any(xx in submission.title.upper() for xx in keyword) and not any(yy in submission.url for yy in ignored_keywords):
                headlines[submission.title] = submission.url
                print(submission.title, submission.url)
    return headlines

if __name__=="__main__":
    print(checkout_subreddit())