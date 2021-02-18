There are 4 components in the creation of this pipeline.

1. Twitter API - This will publish the tweet data to the Kafka Cluster.

2. Kafka Server - The server publishes the data gathered from the producer.

3. Spark - This will help in data processing and ingestion of data to the database.

4. Hive - This is the database,where we will keep the store the final processed data.


# Prerequisite

1. Kafka & Zookeeper

2. Hadoop

3. Spark

4. Hive

# Steps to run the pipeline.


1. Terminal 1 - Zookeeper

We need to start a Zookeeper instance.

```bash
~$ cd kafka/
~/kafka$ bin/zookeeper-server-start.sh config/zookeeper.properties
```

2. Terminal 2 -- Kafka Broker

We need to start the Kafka broker.

```bash
~$ cd kafka/
~/kafka$ bin/kafka-server-start.sh config/server.properties
```

3. Terminal 3 -- Kafka Config

We need to create the topic that will hold our tweets.

```bash
~/kafka$ bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic tweet_stream
```

4. Terminal 4 -- Hive Metastore

``` bash
~$ hive --services metastore
```

There shouldn't be much output besides a message that says the metastore server has started.

5. Terminal 5 -- Hive

Make the database for storing our Twitter data:

``` bash
hive> CREATE TABLE tweets (text STRING, words INT, length INT)
    > ROW FORMAT DELIMITED FIELDS TERMINATED BY '\\|'
    > STORED AS TEXTFILE;
```

You can use `SHOW TABLES;` to double check that the table was created.


```bash
~$ hive

 ...

hive> use default;
hive> select count(*) from tweets;
```

6. Terminal 6 -- Stream Producer

Stream Producer - Run the `fake_tweet_gen.py` script to generate fake tweets. You can also run `real_tweets.py` script with the necessary twitter API keys to collect tweets from your account.

```bash
~$ python3 real_tweets.py
```

7. Terminal 7 -- Stream Consumer + Spark Stream

```bash
~$ spark-submit --jars spark-streaming-kafka-0-8-assembly_2.11-2.4.3.jar spark_stream.py
```

Next, go back to "Terminal #5 (Hive shell), and run the `select count(*)` to see if the data is being written to Hive. If you get something greater than zero, it's working!