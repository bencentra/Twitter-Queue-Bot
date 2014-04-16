from peewee import * 
import json
db = SqliteDatabase('tweets.db', threadlocals=True)

class Tweet(Model):
    content = CharField()

    def __str__(self):
        return json.dumps({"content":self.content, "id":self.id})

    class Meta():
        database = db

def addTweet(content=""):
    if not content:
        return
    return Tweet.create(content=content)

def allTweetSelectQuery():
    return Tweet.select().order_by(Tweet.id)

def allTweets():
    return [tweet for tweet in allTweetSelectQuery()]

def allTweetDicts():
    return [dictionaryForTweet(tweet) for tweet in allTweetSelectQuery()]

def dictionaryForTweet(tweet):
    return vars(tweet)["_data"]

def numberOfTweets():
    return Tweet.select().count()

def topTweet():
    tweets = (Tweet
            .select()
            .order_by(Tweet.id)
            .limit(1))
    if not tweets:
        return None
    return tweets.first()

def popFirstTweet():
    tweet = topTweet()
    if not tweet:
        print("Tweet doesn't exist.")
        return None

    numberDeleted = tweet.delete_instance()

    if numberDeleted < 1:
        print("Tweet not deleted.")
        return None

    return tweet

Tweet.create_table(True)
