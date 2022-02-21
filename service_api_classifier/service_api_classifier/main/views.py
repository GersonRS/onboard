from datetime import datetime
from typing import Dict
import aiohttp_jinja2
from aiohttp import web
from pandas import DataFrame

from service_api_classifier.database import COLLECTION, get_database
from service_api_classifier.models import get_model


@aiohttp_jinja2.template("index.html")
async def index(request: web.Request) -> Dict[str, str]:
    results = get_database().onboard_classifier.find()
    return {"results": results}

@aiohttp_jinja2.template("create.html")
async def create(request: web.Request) -> Dict[str, str]:
    return {"results": None}

async def store(request):

    if request.method == 'POST':
        form = await request.post()
        data = {}
        values = list(map(lambda x: float(x), form.values()))
        for key, value in form.items():
            data[key] = [float(value)]
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
        raise web.HTTPFound(location=request.app.router['index'].url_for())

    return {}