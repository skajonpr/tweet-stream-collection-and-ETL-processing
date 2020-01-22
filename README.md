# tweet-stream-collection-and-ETL-processing
<div id="des" class="desclass">
  <h2>Description</h2>
  <p>The program is to collect tweet streams and store them in a MongoDB database. RabbitMQ is used as a message broker to queue the tweets. All applications run on Docker ecosystem.</p>
</div>

The below picture shows the architecture of the applications

<img width="726" alt="data collection" src="https://user-images.githubusercontent.com/45326221/72861752-d5ed0f80-3c98-11ea-97e5-d32b186748c0.png">

<div id="London" class="tabcontent">
  <h3>How it works?</h3>
  <p>&nbsp&nbspTwitter provides an API that allows one to access its data which is available at no cost with limitations and with payments for more access. Generally, two functions of API requests are available for historical and streaming data. In this repo, a Python library called Tweepy, an open source API, was used for data stream requests.</p>
  <p>&nbsp&nbspIn order to make a request, the identification of keywords included in the tweet is required. My requested keywords here was 'Joe Biden'. All retweets were filtered out in this process as duplicate tweets are undesired in my analysis. Each tweet included data of username, screen name, text, hashtag, location, and tweeted time were stored in NoSQL database (MongoDB). All applications were run inside Docker containers.</p>
  <p>&nbsp&nbspThe RabbitMQ is a message broker which was responsible for handling and queuing data streams that were too overwhelming and that made the data storing process unable to keep up with the incoming data and eventually crashed. RabbitMQ works in incorporation with its producer and consumer which are responsible for enqueuing and
dequeuing messages (tweets in this context).</p>
  
</div>
