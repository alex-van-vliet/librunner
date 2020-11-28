from multiprocessing.connection import Connection, Client
from typing import List, Tuple, Optional, Any

from .model import Model


class Runner:
    data_: Any
    models_: List[Model]
    address_: Tuple[str, int]
    client_: Optional[Connection]

    def __init__(self, data, models, address):
        self.data_ = data
        self.models_ = models
        self.address_ = address
        self.client_ = None

    def __enter__(self):
        self.client_ = Client(self.address_)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client_.close()

    def __call__(self):
        while True:
            data = self.client_.recv()
            if data is None:
                break
            model, parameters = data
            result = self.models_[model].create(parameters)(self.data_)
            self.client_.send((model, parameters, result,))
