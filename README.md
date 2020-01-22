# tweet-stream-collection-and-ETL-processing
The program is to collect tweet streams and store them in a MongoDB database. RabbitMQ is used as a message broker to queue the tweets. All applications run on Docker ecosystem.

The below picture shows the architecture of the applications

<img width="726" alt="data collection" src="https://user-images.githubusercontent.com/45326221/72861752-d5ed0f80-3c98-11ea-97e5-d32b186748c0.png">


Twitter provides an API that allows one to access its data which is available at no
cost with limitations and with payments for more access. Generally, two functions of
API requests are available for historical and streaming data. In this paper, a Python
library called Tweepy, an open source API, was used for data stream requests. In or-
der to make a request, the identification of keywords included in the tweet is required.
Our requested keywords were 'Joe Biden', 'Elizabeth Warren', and 'Bernie Sanders'. All
retweets were ltered out in this process as duplicate tweets are undesired in our anal-
ysis. Each tweet included data of username, screen name, text, hashtag, location, and
tweeted time were stored in NoSQL database (MongoDB). Many modern technologies
were adopted to accommodate all data streams for multiple days. Figure 2 shows the
data collection architecture. All applications were run inside Docker containers set up on AWS. Twitter API re-
quest programs was developed separately for each presidential candidate and run inside
separate Docker containers, since data from each candidate would be analyzed inde-
pendently. The RabbitMQ is a message broker which was responsible for handling and
queuing data streams that were too overwhelming and that made the data storing process
unable to keep up with the incoming data and eventually crashed. RabbitMQ works in
