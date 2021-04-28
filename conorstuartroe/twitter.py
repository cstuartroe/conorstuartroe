import os
import tweepy

TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_TOKEN = os.getenv("TWITTER_TOKEN")
TWITTER_TOKEN_SECRET = os.getenv("TWITTER_TOKEN_SECRET")


auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_TOKEN, TWITTER_TOKEN_SECRET)
api = tweepy.API(auth)


def user_to_json(user):
    return {
        "handle": user.screen_name,
        "name": user.name,
        "pic": user.profile_image_url_https,
    }


def tweet_to_json(status):
    out = {
        "author": user_to_json(status.author),
        "created_at": status.created_at,
        "id": status.id,
    }

    if hasattr(status, "retweeted_status"):
        out["retweeted_status"] = tweet_to_json(status.retweeted_status)
    else:
        out["text"] = status.text

    return out
