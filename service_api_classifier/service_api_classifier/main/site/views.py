from datetime import datetime
from typing import Dict
import aiohttp_jinja2
from aiohttp import web
from pandas import DataFrame
from service_api_classifier.utils.predict_client import predict


@aiohttp_jinja2.template("index.html")
async def index(request: web.Request) -> Dict[str, str]:
    results = list(request.app["db"].onboard_classifier.find())
    return {"results": results}


@aiohttp_jinja2.template("create.html")
async def create(request: web.Request) -> Dict[str, str]:
    return {"results": ""}


async def store(request):

    if request.method == "POST":
        form = await request.post()
        data = {}
        values = list(map(lambda x: float(x), form.values()))
        model = request.app["model"]
        result = predict(values)
        data = {
            "values": values,
            "prediction_name": str(type(model))
            .split(".")[-1]
            .replace("'", "")
            .replace(">", ""),
            "prediction": result,
            "create_at": str(datetime.now()),
        }
        request.app["db"].onboard_classifier.insert_one(data)
        raise web.HTTPFound(location=request.app.router["index"].url_for())

    return None
