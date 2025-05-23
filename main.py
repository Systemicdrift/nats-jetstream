import asyncio
from nats.aio.client import Client as NATS
from nats.js.api import StreamConfig

async def main():
    nc = NATS()
    await nc.connect("nats://nats:4222")  # connect to service name

    js = nc.jetstream()

    try:
        await js.add_stream(name="EVENTS", subjects=["events.*"])
        print("Stream 'EVENTS' created.")
    except Exception as e:
        if "already in use" not in str(e):
            raise
        print("Stream 'EVENTS' already exists.")

    ack = await js.publish("events.created", b"Hello from JetStream!")
    print(f"Published to {ack.stream}, seq: {ack.seq}")

    sub = await js.pull_subscribe("events.*", durable="MY_CONSUMER")
    msgs = await sub.fetch(1, timeout=2)

    for msg in msgs:
        print(f"Received message: {msg.data.decode()}")
        await msg.ack()

    await nc.drain()

if __name__ == "__main__":
    asyncio.run(main())
