__version__ = "0.0.1"

from .app import Server  # noqa: F401
from .grpc_server import Predictor  # noqa: F401
from .generated import predict_pb2  # noqa: F401