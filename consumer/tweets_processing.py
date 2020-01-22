import pymongo
import pika
import json
import time


# define function to collect tweets
def store_tweets(tweet):
    collection.insert_one(tweet)


def callback(ch, method, properties, body):
    store_tweets(json.loads(body))



if __name__ == '__main__':

    # wait for connection to db to be established
    while True:
        try:

            # establish connection to database and create collection
            client = pymongo.MongoClient("mongodb://mongo_db:27017")
            collection = client['joebiden']['ts_joebiden']
            break

        except:
            time.sleep(10)


    # wait for connection to RabbitMQ server to be established
    while True:
        try:
            # establish connection and queue on RabbitMQ
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbit'))
            channel = connection.channel()

            channel.queue_declare(queue='tweets_queue')
            break

        except:
            time.sleep(10)

    # consume messages
    channel.basic_consume(queue='tweets_queue', on_message_callback=callback, auto_ack=True)

    channel.start_consuming()
