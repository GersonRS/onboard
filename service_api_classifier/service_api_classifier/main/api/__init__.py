from os import name
from aiohttp import web
from .handlers import results, predict


def init_app(app):
    app.add_routes(
        [web.get("/results", results, name="results"), web.post("/predict", predict, name="predict")]
    )
