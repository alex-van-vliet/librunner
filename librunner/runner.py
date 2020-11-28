from multiprocessing.connection import Connection
from typing import List

from .model import Model


class Runner:
    models_: List[Model]
    pipe_: Connection

    def __init__(self, models, pipe):
        self.models_ = models
        self.pipe_ = pipe

    def __call__(self):
        while True:
            data = self.pipe_.recv()
            if data is None:
                break
            model, parameters = data
            result = self.models_[model].create(parameters)()
            self.pipe_.send((model, parameters, result,))
