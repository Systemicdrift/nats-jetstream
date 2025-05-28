# test_integration.py
import pytest
import httpx
import asyncio

@pytest.mark.asyncio
async def test_publish_and_consume():
    async with httpx.AsyncClient(base_url="http://app:8000") as client:
        # Step 1: Publish a message
        resp = await client.post("/publish/", json={"subject": "events.created", "message": "test123"})
        assert resp.status_code == 200
        ack = resp.json()
        assert ack["stream"] == "EVENTS"

        # Step 2: Trigger consumer
        resp = await client.get("/consume/", params={"count": 1})
        assert resp.status_code == 200
        assert "Consuming" in resp.json()["status"]

        # Give some time for background task to run
        await asyncio.sleep(2)
