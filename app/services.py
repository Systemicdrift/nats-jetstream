import asyncio
from fastapi import FastAPI, BackgroundTasks
from nats.aio.client import Client as NATS
from nats.js.api import StreamConfig
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse

nc = NATS()
js = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global js
    await nc.connect("nats://nats:4222")
    js = nc.jetstream()

    try:
        await js.add_stream(name="EVENTS", subjects=["events.*"])
        print("Stream 'EVENTS' created.")
    except Exception as e:
        if "already in use" not in str(e):
            raise
        print("Stream 'EVENTS' already exists.")

    yield  # <-- App runs between startup and shutdown

    await nc.drain()
    print("NATS connection drained.")

app = FastAPI(lifespan=lifespan)

@app.post("/publish/")
async def publish_message(subject: str = "events.created", message: str = "Hello from FastAPI"):
    ack = await js.publish(subject, message.encode())
    return {"stream": ack.stream, "seq": ack.seq}

@app.get("/consume/")
async def consume_messages(count: int = 1, background_tasks: BackgroundTasks = None):
    async def _consume():
        sub = await js.pull_subscribe("events.*", durable="MY_CONSUMER")
        msgs = await sub.fetch(count, timeout=2)
        for msg in msgs:
            print(f"Received: {msg.data.decode()}")
            await msg.ack()

    background_tasks.add_task(_consume)
    return {"status": f"Consuming {count} messages from 'events.*'"}

@app.get("/healthz")
async def health_check():
    if nc.is_connected:
        return {"status": "ok"}
    return JSONResponse(status_code=503, content={"status": "nats disconnected"})
