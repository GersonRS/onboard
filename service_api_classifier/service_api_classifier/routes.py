import pathlib

from aiohttp import web

from service_api_classifier.main import site, api

PROJECT_PATH = pathlib.Path(__file__).parent


def init_routes(app: web.Application) -> None:
    add_route = app.router

    # added static dir
    add_route.add_static(
        "/static/",
        path=(PROJECT_PATH / "static"),
        name="static",
    )

    api.init_app(app)
    site.init_app(app)
