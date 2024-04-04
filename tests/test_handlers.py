import pytest


@pytest.mark.asyncio
async def test_ping(client):
    response = await client.get("http://127.0.0.1:8000/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong"}


@pytest.mark.asyncio
async def test_create_short_url(client):
    data = {"url": "https://www.example.com"}
    response = await client.post('http://127.0.0.1:8000/url/', json=data)

    assert response.status_code == 200
