import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch

from app.services import app

@pytest.mark.asyncio
@patch("app.services.js")
async def test_publish_message(mock_js):
    mock_ack = AsyncMock()
    mock_ack.stream = "EVENTS"
    mock_ack.seq = 1
    mock_js.publish = AsyncMock(return_value=mock_ack)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/publish/", params={"subject": "events.created", "message": "Test"})
        assert response.status_code == 200
        assert response.json() == {"stream": "EVENTS", "seq": 1}

@pytest.mark.asyncio
@patch("app.services.js")
async def test_consume_messages(mock_js):
    mock_msg = AsyncMock()
    mock_msg.data.decode.return_value = "Mock message"
    mock_msg.ack = AsyncMock()

    mock_sub = AsyncMock()
    mock_sub.fetch.return_value = [mock_msg]
    mock_js.pull_subscribe = AsyncMock(return_value=mock_sub)

    async def fake_add_task(task_fn, *args, **kwargs):
        await task_fn(*args, **kwargs)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        with patch("app.services.BackgroundTasks.add_task", new=fake_add_task):
            response = await client.get("/consume/", params={"count": 1})
            assert response.status_code == 200
            assert response.json() == {"status": "Consuming 1 messages from 'events.*'"}