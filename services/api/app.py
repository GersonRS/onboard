from datetime import datetime
import json
import os
import pickle
from aiohttp import web
from pandas import DataFrame
from pymongo import MongoClient
from bson.json_util import dumps

CONNECTION_STRING = 'mongodb://' + os.environ.get("MONGODB_USERNAME", "admin") + ':' + os.environ.get("MONGODB_PASSWORD", "admin") + '@' + os.environ.get("MONGODB_HOSTNAME", "localhost") + ':27017'
COLLECTION = os.environ.get("MONGODB_DATABASE", "onboard")

__model = None
__db = None

def get_model():
    global __model
    if __model is None:
        with open(os.path.dirname(__file__)+'/model_pkl', 'rb') as f:
            __model = pickle.load(f)
    return __model


def get_database(collection):
    global __db
    if __db is None:
        __db = MongoClient(CONNECTION_STRING)
    return __db[collection]


async def results(request):
    results = list(get_database(COLLECTION).requests.find())
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
        "create_at": str(datetime.now())
    }
    x = get_database(COLLECTION).onboard_classifier.insert_one(data)
    response_obj = {'id': str(x.inserted_id)}
    return web.json_response(response_obj, status=200)

app = web.Application()
app.add_routes([web.get('/results', results),
                web.post('/predict', predict)])

if __name__ == '__main__':
    web.run_app(app)
