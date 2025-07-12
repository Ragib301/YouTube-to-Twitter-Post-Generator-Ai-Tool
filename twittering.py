import tweepy
from api_key import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET, BEARER_TOKEN


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(
    ACCESS_KEY,
    ACCESS_SECRET,
)

newapi = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    access_token=ACCESS_KEY,
    access_token_secret=ACCESS_SECRET,
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
)
api = tweepy.API(auth)


def post_on_twitter(content, image_path):
    media = api.media_upload(image_path)
    post_result = newapi.create_tweet(text=content, media_ids=[media.media_id])
    return post_result


if __name__ == "__main__":
    sampletweet = f"""Day 1 of testing twitter:
    Why did the computer apply for a job at the bakery? 🍞 It wanted to work on its 'bread'ware skills! 😂 #TechHumor #BakingBytes #ProgrammingPuns
    I wanted to test a tweet and if you are seeing this, I have successfully completed the post. Yay!"""
    response = post_on_twitter(sampletweet, "Post Images/image_0.png")
    print(response)
