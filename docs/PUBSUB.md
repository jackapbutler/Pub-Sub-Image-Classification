# Pub Sub

Now that the model is trained we can setup the Kafka Pub-Sub architecture. The messages within this ML system will be sent/received using a stream processing architecture. There are two implementation options:

1. A locally hosted [Apache Kafka](https://kafka.apache.org/).

2. A Google Cloud Platform [Pub/Sub](https://cloud.google.com/pubsub).

## Apache Kafka

To setup Kafka follow the steps below:

1. Install [Java](https://www.oracle.com/java/technologies/downloads/) in order to run the Kafka executables.
2. Download Kafka’s binaries from the official [download page](https://archive.apache.org/dist/kafka/3.0.0/kafka_2.13-3.0.0.tgz) (this one is for v3.0.0).
3. Extract the tar files (inside of the appropriate directory): `tar -xvzf kafka_2.13-3.0.0.tgz`.
4. Run the servers:

   a) Run Zookeeper for state management: `bin/zookeeper-server-start.sh config/zookeeper.properties`

   b) Kafka for data storage and distribution: `bin/kafka-server-start.sh config/server.properties`

5. We will need to create one topic called `fashion-images` for this assignment.

- Create a topic by running `bin/kafka-topics.sh --create --topic fashion-images --bootstrap-server localhost:9092 --replication-factor 1 --partitions 4`.

> List all created topics with `bin/kafka-topics.sh --list --bootstrap-server localhost:9092`.

> Describe a certain topic with `bin/kafka-topics.sh --describe --topic fasion-images --bootstrap-server localhost:9092`.

> Delete a topic with `bin/kafka-topics.sh --delete --topic fashion-images --bootstrap-server localhost:9092`

6. To setup Kafka you will need a [Producer](../kafka_producer.py) and [Consumer](../kafka_consumer.py).

- The Producer will be controlled inside `model_app.py` in the `Inference` page and does not need any prior setup.

  > Press `Send Image` to send the uploaded image to the `fashion-images` topic for predictions.

- To setup the Consumer, open up a terminal instance and run `streamlit run results_app.py`.

  > Press `Start Listening` to initialise a Consumer which will read from the `fashion-images` topic and perform predictions.

## Google Cloud Pub/Sub

To setup GCP Pub/Sub follow the steps below:

1. Create a project on GCP and enable the [Pub/Sub](https://cloud.google.com/pubsub) API.

2. Create a service account with a `secret-key.json` file for accessing GCP.

3. Create a topic on GCP Pub/Sub called `fashion-images`.

4. The code in `gcp_consumer.py` replicates the same structure as `kafka_consumer.py`.

5. The code in `gcp_producer.py` replicates the same structure as `kafka_producer.py`.

> Once you follow the steps above you should be able to swap the `KafkaImage<USE CASE>` for the respective `GCPImage<USE CASE>` classes.

> You can test this GCP Pub/Sub system in the [`gcp_pubsub_test.py`](../gcp_pubsub_test.py) file
