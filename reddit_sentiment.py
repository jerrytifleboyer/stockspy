import json
import praw 

subreddit_list = ['wallstreetbets', 'stocks', 'investing', 'stockmarket']

def login_to_reddit():
    with open('config/pw.json') as pw:
        data = json.load(pw)
        reddit = praw.Reddit(
            client_id=data['reddit']['account'], 
            client_secret=data['reddit']['secret'], 
            user_agent=data['reddit']['alias'])
    return reddit
reddit = login_to_reddit()

def check_subreddits():
    for subreddit in subreddit_list:
        print(subreddit)
        for submission in reddit.subreddit(subreddit).new(limit=100):
            print(submission.title)
check_subreddits()