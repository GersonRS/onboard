from typing import Protocol


class ScikitModel(Protocol):
    def predict(self, X):
        ...
