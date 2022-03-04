from aiohttp import web
from datetime import datetime
import json
from bson.json_util import dumps
from pandas import DataFrame


async def results(request):
    results = list(request.app["db"].onboard_classifier.find())
    return web.json_response(json.loads(dumps(results)))


async def predict(request):
    data = await request.json()
    values = list(data.values())
    for d in data:
        data[d] = [data.get(d)]
    dataframe = DataFrame(data)
    model = request.app["model"]
    result = model.predict(dataframe)
    data = {
        "values": values,
        "prediction_name": str(type(model))
        .split(".")[-1]
        .replace("'", "")
        .replace(">", ""),
        "prediction": result[0],
        "create_at": str(datetime.now()),
    }
    request.app["db"].onboard_classifier.insert_one(data)
    return web.json_response(result[0], status=200)
