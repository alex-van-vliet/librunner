from typing import List

from .model import Model
from .process import Process


class Runner:
    process_: Process
    models_: List[Model]

    def __init__(self, process, models):
        self.process_ = process
        self.models_ = models

    def __call__(self):
        while True:
            data = self.process_.recv(0)
            if data is None:
                break
            model, parameters = data
            result = self.models_[model].create(parameters)()
            self.process_.send(0, (model, parameters, result))
