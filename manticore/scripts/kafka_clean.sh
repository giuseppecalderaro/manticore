#!/usr/bin/env bash

kill $(ps aux | grep -i "Dzookeeper" | grep -v "grep" | awk '{ print $2 }') &> /dev/null || echo 'Zookeeper is not running'
rm -rf /usr/local/var/run/zookeeper/data
rm -rf /usr/local/var/lib/kafka-logs
