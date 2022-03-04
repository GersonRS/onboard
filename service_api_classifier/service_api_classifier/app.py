import pickle
import os
from pathlib import Path
from typing import (
    AsyncGenerator,
    Optional,
    List,
)

import aiohttp_jinja2
from aiohttp import web
import jinja2
from pymongo import MongoClient

from service_api_classifier.routes import init_routes
from service_api_classifier.utils.common import (
    COLLECTION,
    CONNECTION_STRING,
    init_config,
)


path = Path(__file__).parent


def init_jinja2(app: web.Application) -> None:
    """
    Initialize jinja2 template for application.
    """
    aiohttp_jinja2.setup(
        app, loader=jinja2.FileSystemLoader(str(path / "templates"))
    )


async def database(app: web.Application) -> AsyncGenerator[None, None]:
    """
    A function that, when the server is started, connects to mongo,
    and after stopping it breaks the connection (after yield)
    """
    db = MongoClient(CONNECTION_STRING)
    app["db"] = db[COLLECTION.strip()]
    yield
    db.close()


async def model(app: web.Application) -> AsyncGenerator[None, None]:
    """
    A function that, when the server is started, load to model,
    and after stopping it close the archive (after yield)
    """
    file = open(os.path.dirname(__file__) + "/models/model_pkl", "rb")
    app["model"] = pickle.load(file)
    yield
    file.close()


def init_app(config: Optional[List[str]] = None) -> web.Application:
    app = web.Application()

    init_jinja2(app)
    init_config(app, config=config)
    init_routes(app)

    app.cleanup_ctx.extend([database, model])

    return app
