# import os
# import pickle

# from service_api_classifier.utils.types import ScikitModel

# __model = None


# def get_model() -> ScikitModel:
#     global __model
#     if __model is None:
#         with open(os.path.dirname(__file__) + "/model_pkl", "rb") as f:
#             __model = pickle.load(f)
#     return __model
