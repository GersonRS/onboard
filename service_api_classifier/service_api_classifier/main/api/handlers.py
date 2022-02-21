from aiohttp import web
from datetime import datetime
import json
from bson.json_util import dumps
from pandas import DataFrame
from service_api_classifier.database import COLLECTION, get_database
from service_api_classifier.models import get_model


async def results(request):
    results = list(get_database().onboard_classifier.find())
    return web.json_response(json.loads(dumps(results)))


async def predict(request):
    data = await request.json()
    values = list(data.values())
    for d in data:
        data[d] = [data.get(d)]
    dataframe = DataFrame(data)
    model = get_model()
    result = model.predict(dataframe)
    data = {
        "values": values,
        "prediction_name": COLLECTION,
        "prediction": result[0],
        "create_at": str(datetime.now()),
    }
    get_database().onboard_classifier.insert_one(data)
    return web.json_response(result[0], status=200)
