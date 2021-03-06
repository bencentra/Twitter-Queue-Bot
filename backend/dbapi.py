from peewee import *
import json
db = SqliteDatabase('tweets.db', threadlocals=True)

class Tweet(Model):
    content = CharField()
    order = IntegerField()

    class Meta():
        database = db

def addTweet(content=""):
    return insertTweet(content, numberOfTweets())

def insertTweet(content, index):
    if not content:
        return None
    if index > numberOfTweets():
        return None

    updateQuery = (Tweet.update(order=(Tweet.order + 1))
                        .where(Tweet.order >= index))
    updateQuery.execute()

    tweet = Tweet.create(content=content, order=index)
    if not tweet:
        return None

    return tweet

def allTweetSelectQuery():
    return Tweet.select().order_by(Tweet.order)

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
            .order_by(Tweet.order)
            .limit(1))
    if not tweets:
        return None
    return tweets.first()

def popFirstTweet():
    tweet = topTweet()
    if not tweet:
        return None
    removeTweet(tweet)
    return tweet

def moveTweet(fromIndex, toIndex):
    if fromIndex == toIndex:
        return None

    count = numberOfTweets()
    if fromIndex > count or toIndex > count:
        return None

    tweet = (Tweet.select()
                  .where(Tweet.order == fromIndex)
                  .limit(1)
                  .first())
    if not tweet:
        return None

    movingDown = fromIndex > toIndex

    if (movingDown):
        firstIndexSelectionQuery = Tweet.order < fromIndex
        secondIndexSelectionQuery = Tweet.order >= toIndex
    else:
        firstIndexSelectionQuery = Tweet.order > fromIndex
        secondIndexSelectionQuery = Tweet.order <= toIndex

    increment = 1 if movingDown else -1

    updateQuery = (Tweet.update(order=(Tweet.order + increment))
                        .where(firstIndexSelectionQuery)
                        .where(secondIndexSelectionQuery))
    updateQuery.execute()

    tweet.order = toIndex
    tweet.save()
    return tweet

def removeTweet(tweet):
    numberDeleted = tweet.delete_instance()
    if numberDeleted == 0:
        return None
    updateQuery = (Tweet.update(order=(Tweet.order - 1))
                        .where(Tweet.order > tweet.order))
    updateQuery.execute()
    return tweet

def removeTweetWithID(id):
    tweet = Tweet.select().where(Tweet.id == id).first()
    if not tweet:
        return None
    return removeTweet(tweet)

Tweet.create_table(True)
