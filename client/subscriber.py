import asyncio
import signal
from gmqtt import Client as MQTTClient


STOP = asyncio.Event()
ASYNC_QUEUE = asyncio.Queue(maxsize=50) 
COUNTER = 0

def on_connect(client, flags, rc, properties):
    print('Connected')

async def on_message(client, topic, payload, qos, properties):
    await ASYNC_QUEUE.put(payload)
    return 0

def on_disconnect(client, packet, exc=None):
    print('Disconnected')

def on_subscribe(client, mid, qos, properties):
    print('Subscribed')

def ask_exit(*args):
    STOP.set()

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
