import tweepy
from app.core.config import settings


def auth_twitter_token(twitter_user_id, access_token, access_token_secret):
    auth = tweepy.OAuth1UserHandler(
        settings.CONSUMER_KEY, settings.CONSUMER_SECRET, access_token, access_token_secret
    )
    api = tweepy.API(auth)
    auth_result = api.verify_credentials()
    return str(auth_result.id) == str(twitter_user_id), twitter_user_id
