import os
import tweepy
from dotenv import load_dotenv

from utils.date import now

load_dotenv()

# TWITTER API CREDENTIALS 
consumerKey = os.environ.get("CONSUMER_KEY")
consumerSecret = os.environ.get("CONSUMER_SECRET")
accessToken = os.environ.get("ACCESS_TOKEN")
accessTokenSecret = os.environ.get("ACCESS_TOKEN_SECRET")

auth = tweepy.OAuth1UserHandler(
    consumerKey,
    consumerSecret,
    accessToken,
    accessTokenSecret
)
client = tweepy.API(auth)

# The app and the corresponding credentials must have the Write permission
def tweet(text, media = None):
    if media == None:
        response = client.update_status(
            status = text
        )
    else:
        media_file = client.media_upload(filename = media)
        response = client.update_status(status = text, media_ids = [media_file.media_id_string])
        print('Tweeted.................................', now())
