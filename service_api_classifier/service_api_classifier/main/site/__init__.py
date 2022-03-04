from aiohttp import web
from service_api_classifier.main.site.views import create, index, store


def init_app(app: web.Application) -> None:
    app.add_routes(
        [
            web.get("/", index, name="index"),
            web.get("/create", create, name="create"),
            web.post("/store", store, name="store"),
        ]
    )
