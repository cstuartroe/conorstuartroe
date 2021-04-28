import praw
import time
import datetime

reddit = praw.Reddit(client_id='PTofuEjEjIPbcg',
                     client_secret='_R0b3zmCvjXGPseYbaPIUEnZAlU',
                     password='LinguisticsIsCool208',
                     user_agent='testscript by /u/conor_emily_ling208',
                     username='conor_emily_ling208')

def get_worthwhile_posts():
    current = time.time()
    reddit.read_only = True
    rWP = reddit.subreddit('WritingPrompts')
    posts = []

    for submission in rWP.new(limit=500):
        timestamp = submission.created
        elapsed = int(current - timestamp + 28800)
        score = submission.score
        if (elapsed < 86400) and (score >= 4) and (elapsed/score < 3600) and (submission.num_comments <= 1):
            posts.append((submission.title,submission.url,score,elapsed//3600))

    return posts
