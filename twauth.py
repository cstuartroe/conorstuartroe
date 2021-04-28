import tweepy

# This is meant to be run locally if I need to generate a new Twitter token

twitter_api_key = input("Twitter API Key: ")
twitter_api_secret = input("Twitter API Secret: ")

auth = tweepy.OAuthHandler(
    twitter_api_key,
    twitter_api_secret,
)

print(f"heroku config:set TWITTER_API_KEY={twitter_api_secret} TWITTER_API_SECRET={twitter_api_secret}")
print(f"export TWITTER_API_KEY={twitter_api_key} && export TWITTER_API_SECRET={twitter_api_secret}")

redirect_url = auth.get_authorization_url()
print(redirect_url)
verifier = input("Verifier: ")
auth.request_token['oauth_token_secret'] = verifier

access_token, access_token_secret = auth.get_access_token(verifier)

print(f"heroku config:set TWITTER_TOKEN={access_token} TWITTER_TOKEN_SECRET={access_token_secret}")
print(f"export TWITTER_TOKEN={access_token} && export TWITTER_TOKEN_SECRET={access_token_secret}")
