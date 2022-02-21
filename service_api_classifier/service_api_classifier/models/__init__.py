import os
import pickle

__model = None


def get_model():
    global __model
    if __model is None:
        with open(os.path.dirname(__file__) + "/model_pkl", "rb") as f:
            __model = pickle.load(f)
    return __model
