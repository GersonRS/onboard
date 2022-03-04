import pickle
import os

from pandas import DataFrame
from .generated import predict_pb2, predict_pb2_grpc

file = open(os.path.dirname(__file__) + "/models/model_pkl", "rb")
model = pickle.load(file)


class Predictor(predict_pb2_grpc.PredictServicer):
    def Predict(self, request, context):
        data = {
            "sepal.length": request.request[0],
            "sepal.width": request.request[1],
            "petal.length": request.request[2],
            "petal.width": request.request[3],
        }
        for d in data:
            data[d] = [data.get(d)]
        print(data)
        dataframe = DataFrame(data)
        print(dataframe.head(1))
        result = model.predict(dataframe)
        return predict_pb2.PredictResult(message=result[0])
