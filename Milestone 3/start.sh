#!/bin/bash

wget https://dlcdn.apache.org/zookeeper/zookeeper-3.7.0/apache-zookeeper-3.7.0-bin.tar.gz
wget https://archive.apache.org/dist/kafka/2.5.0/kafka_2.12-2.5.0.tgz
tar -xzvf apache-zookeeper-3.7.0-bin.tar.gz
tar -xzvf kafka_2.12-2.5.0.tgz
rm apache-zookeeper-3.7.0-bin.tar.gz kafka_2.12-2.5.0.tgz


# Run zookeeper
#./apache-zookeeper-3.7.0-bin/bin/zkServer.sh start ./kafka_2.12-2.5.0/config/zookeeper.properties

# Run kafka
#./kafka_2.12-2.5.0/bin/kafka-server-start.sh ./kafka_2.12-2.5.0/config/server.properties


# pip uninstall kafka
# pip install kafka-python

#./kafka_2.12-2.5.0/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic twitter


##############

# Optional
#./kafka_2.12-2.5.0/bin/kafka-topics.sh --list --zookeeper localhost:2181
#./kafka_2.12-2.5.0/bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic twitter
