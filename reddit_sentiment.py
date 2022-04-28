import praw 
import json
import time

# subreddit_list = ['wallstreetbets', 'stocks', 'investing', 'stockmarket']
subreddit_list = ['wallstreetbets']

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
    start = time.time()
    counter= 0

    store_every_post = []
    for subreddit in subreddit_list:
        #you can change this from (hot, new, top, rising)
        for post in reddit.subreddit(subreddit).hot(limit=100):
            store_every_post.append(post.title)

    unique_posts = set(store_every_post)
    for post in unique_posts:
        print(post)
        counter+=1
    #im just managing time
    print(counter)
    end = time.time()
    print(end-start)
    
check_subreddits()