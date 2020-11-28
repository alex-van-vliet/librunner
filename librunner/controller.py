from multiprocessing.connection import Connection, Pipe, wait
from multiprocessing.context import Process
from typing import Generator, Optional, Tuple, Any, List

from .model import Model
from .runner import Runner


def creator(models: List[Model], pipe: Connection):
    runner = Runner(models, pipe)
    runner()


class Controller:
    models_: List[Model]
    generator_: Optional[Generator[Tuple[int, Any], None, None]]
    ended_: bool
    left_: int
    nb_children_: int
    children_: List[Process]
    pipes_: List[Connection]

    def __init__(self, models, nb_children):
        self.models_ = models
        self.generator_ = None
        self.left_ = 0
        self.children_ = []
        self.pipes_ = []
        self.nb_children_ = nb_children

    def __enter__(self):
        for child in range(self.nb_children_):
            parent_conn, child_conn = Pipe()
            self.pipes_.append(parent_conn)
            self.children_.append(Process(target=creator, args=(self.models_, child_conn,)))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for pipe in self.pipes_:
            pipe.send(None)
        for child in self.children_:
            child.join()

    def start(self):
        for child, pipe in zip(self.children_, self.pipes_):
            child.start()
            try:
                data = next(self.generator_)
                self.left_ += 1
                pipe.send(data)
            except StopIteration:
                self.generator_ = None
                break

    def receive(self):
        responses = wait(self.pipes_, None)
        for pipe in responses:
            yield pipe, pipe.recv()

    def __call__(self):
        def models():
            for i, model in enumerate(self.models_):
                for parameters in model():
                    yield i, parameters

        self.left_ = 0
        self.generator_ = models()
        self.start()
        results = []
        while self.left_ > 0:
            for pipe, result in self.receive():
                results.append(result)
                self.left_ -= 1
                if self.generator_:
                    try:
                        data = next(self.generator_)
                        self.left_ += 1
                        pipe.send(data)
                    except StopIteration:
                        self.generator_ = None
        print('Finished.')
        print('Top 3 runs:')
        results = sorted(results, key=lambda v: v[-1], reverse=True)
        for model, parameters, score in results[:3]:
            print(f'Score: {score}, parameters: '
                  + ', '.join(f'{key}={repr(value)}'
                              for key, value
                              in self.models_[model].values(parameters).items()))
