#!/bin/bash

for i in {1..1000}
do
    mosquitto_pub -m ‘{“sensor_value”:$RANDOM}’ -t /events
done 