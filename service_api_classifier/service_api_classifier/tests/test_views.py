from pytest_aiohttp import aiohttp_client


async def test_view(client: aiohttp_client) -> None:
    resp = await client.get("/")

    assert resp.status == 200
    assert "Onboard" in await resp.text()


async def test_restults(client: aiohttp_client) -> None:
    resp = await client.get("/results")

    assert resp.status == 200
    data = await resp.json()
    assert isinstance(data, list)


async def test_predict(client: aiohttp_client) -> None:
    resp = await client.post("/predict")

    assert resp.status == 500
    # data = await resp.json()
    # assert isinstance(data, str)
