import os

import grpc

from service_api_classifier.generated import predict_pb2, predict_pb2_grpc

CONNECTION = (
    os.environ.get("GRPC_HOSTNAME", "processing")
    + ":"
    + os.environ.get("GRPC_PORT", "50051")
)


def predict(values):
    with grpc.insecure_channel(CONNECTION) as channel:
        stub = predict_pb2_grpc.PredictStub(channel)
        response = stub.Predict(
            predict_pb2.PredictRequest(request=values)
        )
    return response.message
