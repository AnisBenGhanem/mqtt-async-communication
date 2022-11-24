# Summary
## 1- Asynchronous Subscriber Script
> ### A- Create our venv
> ### B- Install necessary packages
> ### C- Writing and Explaining the Subscriber Code
## 2- Dockerizing the Challenge
> ### A- Running Mosquitto on Docker and Testing it
> ### B- Dockerizing the Asynchronous Subscriber script
> ### C- Docker Coompose
## 3- Running the project
</br></br></br>



# 1- Asynchronous Subscriber Script

## A- Create our venv
We are creating the venv to isolate our python modules from the computer. A best practice that I have come to learn.

``` shell
python -m venv venv
source venv/bin/activate
```
  
    
      

---
## B- Install necessary packages
``` shell
pip install gmqtt
pip install asyncio
```

---
## C- Writing and Explaining the Subscriber Code
we imported asyncio to run function asynchronously using async/await syntax,
signal library will help use defining custom handlers to be executed when a signal is received, and gmqtt it is a library that allows asynchronous messaging over MQTT.
``` python
import asyncio
import signal
from gmqtt import Client as MQTTClient
```

An asyncio event can be used to notify multiple asyncio tasks that some event has happened.

``` python
STOP = asyncio.Event()
```

asyncio queues are designed to be similar to classes of the queue module. Although asyncio queues are not thread-safe, they are designed to be used specifically in async/await code.

``` python
ASYNC_QUEUE = asyncio.Queue(maxsize=50) 
```

____CALLBACKS____\
Since this is a test, we have only applied async on the on_message function to make it asynchronous.

``` python
def on_connect(client, flags, rc, properties):
    print('Connected')

async def on_message(client, topic, payload, qos, properties):
    await ASYNC_QUEUE.put(payload)
    return 0

def on_disconnect(client, packet, exc=None):
    print('Disconnected')

def on_subscribe(client, mid, qos, properties):
    print('Subscribed')
```

This function will help us exit the program properly

``` python
def ask_exit(*args):
    STOP.set()
```

____Asynchronous function that reads from the queue____

``` python
async def reader():
    global COUNTER
    while not STOP.is_set():
        if not ASYNC_QUEUE.empty():
            message = await ASYNC_QUEUE.get()
            COUNTER= COUNTER+1
            print(
                "message "+str(message.decode("utf-8"))+"\n"
                + f"count = {COUNTER}"
            )
            
        await asyncio.sleep(1)
    print("stopped")
    return 0
```

____Main Function____

``` python
async def main(broker_host):
    client = MQTTClient("client-id")
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.on_subscribe = on_subscribe
    await client.connect(broker_host)
    client.subscribe('/events')
    await reader()
    await STOP.wait()
    await client.disconnect()

if __name__ == '__main__':
    loop = asyncio.new_event_loop()

    host = 'mosquitto'

    loop.add_signal_handler(signal.SIGINT, ask_exit)
    loop.add_signal_handler(signal.SIGTERM, ask_exit)

    loop.run_until_complete(main(host))
```


---


# 2- Dockerizing the Challenge

## A- Running Mosquitto on Docker and Testing it

First, we need to pull Mosquitto's image.

``` shell
docker pull eclipse-mosquitto 
```

This will pull [Dockerhub's Mosquitto image](https://hub.docker.com/_/eclipse-mosquitto).

Now, we need to run it and bind the container's 1883 port to ours to be able to interact with Mosquitto.

``` shell
docker run -p 1883:1883 -v /home/anis/Desktop/mosquitto-test/config/mosquitto.conf:/mosquitto/config/mosquitto.conf eclipse-mosquitto
```

To test that all works great, just run the following:

``` shell
mosquitto_sub -t test_queue
```
---


## B- Dockerizing the Asynchronous Subscriber script
As a first step, we prepared the dockerfile 
``` docker
FROM python

COPY requirements.txt requirements.txt

RUN python3 -m pip install -r requirements.txt

COPY subscriber.py subscriber.py

CMD ["python3","-u","subscriber.py"]
```
then, we built the docker image for the subscriber script and named it livello-challenge 
``` shell
docker build -t livello-challenge client/.
```
---
## C- Docker Compose
We prepared the docker-compose file.
``` docker
version: '3'
services:
  mosquitto:
    image: eclipse-mosquitto
    volumes:
      - ./config/mosquitto.conf:/mosquitto/config/mosquitto.conf
    ports:
      - 1883:1883
  livello-product:
    image: anisbg/async-communication:livelloChallenge
    depends_on:
      - mosquitto
```
and finally, run this docker compose file by typing
``` shell
docker-compose up
```

---
# 3- Running the project
install mosquitto client
``` shell
sudo apt-get install mosquitto-clients
```


Clone this project [Livello Challenge](https://github.com/AnisBenGhanem/mqtt-async-communication).

Run docker-compose
``` shell
docker-compose up
```

Run the publisher script
``` shell
bach publisher.sh
```