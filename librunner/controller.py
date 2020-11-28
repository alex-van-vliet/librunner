from multiprocessing.connection import Connection, wait, Listener
from multiprocessing.context import Process
from typing import Generator, Optional, Tuple, Any, List

from .model import Model
from .runner import Runner


def creator(data: Any, models: List[Model], address: Tuple[str, int]):
    with Runner(data, models, address) as runner:
        runner()


class Controller:
    data_: Any
    models_: List[Model]
    generator_: Optional[Generator[Tuple[int, Any], None, None]]
    ended_: bool
    left_: int
    nb_children_: int
    children_: List[Process]
    address_: Tuple[str, int]
    listener_: Optional[Listener]
    clients_: List[Connection]
    results_: List[Tuple[int, List[int], float]]

    def __init__(self, data, models, nb_children, address):
        self.data_ = data
        self.models_ = models
        self.generator_ = None
        self.left_ = 0
        self.children_ = []
        self.nb_children_ = nb_children
        self.address_ = address
        self.listener_ = None
        self.clients_ = []
        self.results_ = []

    def results(self):
        return self.results_

    def __enter__(self):
        self.listener_ = Listener(self.address_, family='AF_INET')
        for child in range(self.nb_children_):
            process = Process(target=creator, args=(self.data_, self.models_, self.address_,))
            process.start()
            self.children_.append(process)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for client in self.clients_:
            client.send(None)
            client.close()
        for child in self.children_:
            child.join()
        self.listener_.close()

    def __call__(self):
        def models():
            for i, model in enumerate(self.models_):
                for parameters in model():
                    yield i, parameters

        self.generator_ = models()
        self.left_ = 0
        self.results_ = []
        while self.generator_ or self.left_ > 0:
            for source in wait([self.listener_._listener._socket, *self.clients_]):
                if source == self.listener_._listener._socket:
                    source = self.listener_.accept()
                    self.clients_.append(source)
                else:
                    self.results_.append(source.recv())
                    self.left_ -= 1
                if self.generator_:
                    try:
                        data = next(self.generator_)
                        self.left_ += 1
                        model, parameters = data
                        print(f'Running: '
                              + ', '.join(f'{key}={repr(value)}'
                                          for key, value
                                          in self.models_[model].values(parameters).items()))
                        source.send(data)
                    except StopIteration:
                        self.generator_ = None
                if not self.generator_:
                    source.send(None)
                    source.close()
                    self.clients_.remove(source)

        self.results_ = sorted(self.results_, key=lambda v: v[-1], reverse=True)
