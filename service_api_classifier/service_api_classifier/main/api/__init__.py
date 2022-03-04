from aiohttp import web
from service_api_classifier.main.api.handlers import predict, results


def init_app(app: web.Application) -> None:
    app.add_routes(
        [
            web.get("/results", results, name="results"),
            web.post("/predict", predict, name="predict"),
        ]
    )
