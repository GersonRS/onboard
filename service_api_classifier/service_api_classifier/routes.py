import pathlib

from aiohttp import web

from service_api_classifier.main.views import index, create, store
from service_api_classifier.main import api

PROJECT_PATH = pathlib.Path(__file__).parent


def init_routes(app: web.Application) -> None:
    add_route = app.router.add_route

    add_route("*", "/", index, name="index")
    add_route("GET", "/create", create, name="create")
    add_route("POST", "/store", store, name="store")

    # added static dir
    app.router.add_static(
        "/static/",
        path=(PROJECT_PATH / "static"),
        name="static",
    )

    api.init_app(app)
