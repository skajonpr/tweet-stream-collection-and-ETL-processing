import tweepy
import tweets_credential as cr
import pika
import json
import time


# Create tweets stream listener
class MyStreamListener(tweepy.StreamListener):

    # define a function to handle stream data
    def on_status(self, status):

        # define variable to store hashtags
        store_hashtags = []

        # check if tweet is retweeted or not. --> if yes, skip the it
        try:
            if status.retweeted_status:
                return
        except:
            # check if tweet is being cut off or not
            # if it's cut off, use text from extended_tweet
            # (too long tweets can be cut off by Twitter)
            try:
                if status.extended_tweet:

                    writing_tweet = {}

                    writing_tweet['created_at'] = status.created_at

                    writing_tweet['user_name'] = status.user.name

                    writing_tweet['screen_name'] = status.user.screen_name

                    writing_tweet['text'] = status.extended_tweet['full_text']

                    writing_tweet['location'] = status.user.location

                    # collect hashtags
                    if len(status.extended_tweet['entities']['hashtags']) >= 1:
                        for hashtag in range(len(status.extended_tweet['entities']['hashtags'])):
                            store_hashtags.append(status.extended_tweet['entities']['hashtags'][hashtag]['text'])

                    writing_tweet['hashtags'] = store_hashtags

            # if tweet not cut off
            # use text from text
            except:

                writing_tweet = {}

                writing_tweet['created_at'] = status.created_at

                writing_tweet['user_name'] = status.user.name

                writing_tweet['screen_name'] = status.user.screen_name

                writing_tweet['text'] = status.text

                writing_tweet['location'] = status.user.location

                # collect hashtags
                if len(status.entities['hashtags']) >= 1:
                    for hashtag in range(len(status.entities['hashtags'])):
                        store_hashtags.append(status.entities['hashtags'][hashtag]['text'])

                writing_tweet['hashtags'] = store_hashtags

        # send messages to RabbitMQ server
        channel.basic_publish(exchange='', routing_key='tweets_queue', body=json.dumps(writing_tweet, default=str))

    # define a function to handle error from exceeding rate limit
    def on_error(self, status_code):
        if status_code == 420:
            # stop program when exceeding rate limit
            return False



if __name__ == "__main__":

    # Authenticate Twitter API user
    auth = tweepy.OAuthHandler(cr.CONSUMER_KEY, cr.CONSUMER_SECRET)
    auth.set_access_token(cr.ACCESS_TOKEN, cr.ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)

    # wait for connection to RabbitMQ server to be established
    while True:
        try:
            # establish connection and queue on RabbitMQ
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbit', heartbeat=600))
            channel = connection.channel()

            channel.queue_declare(queue='tweets_queue')


            # call stream listener
            myStreamListener = MyStreamListener()
            # request for Twitter API
            myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

            # filter tweets by keywords and languages
            myStream.filter(languages=["en"], track=['Joe Biden', 'Biden'], is_async=False)


        except:
            time.sleep(10)


