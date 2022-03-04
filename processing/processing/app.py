from concurrent import futures
import grpc

from .generated import predict_pb2_grpc
from .grpc_server import Predictor


class Server:

    @staticmethod
    def run():
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        predict_pb2_grpc.add_PredictServicer_to_server(Predictor(), server)
        server.add_insecure_port('[::]:50051')
        server.start()
        server.wait_for_termination()