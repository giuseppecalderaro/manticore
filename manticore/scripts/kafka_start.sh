#!/usr/bin/env bash

sudo mkdir -p /usr/local/var/run/zookeeper/data
sudo chmod 777 /usr/local/var/run/zookeeper/data
zkServer start

mkdir -p /usr/local/var/lib/kafka-logs
sudo chmod 777 /usr/local/var/lib/kafka-logs
/usr/local/bin/kafka-server-start /usr/local/etc/kafka/server.properties
