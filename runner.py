import time

from librunner.model import Model
from librunner.main import main


class ExampleModel:
    first_: int
    second_: int

    def __init__(self, first, second):
        self.first_ = first
        self.second_ = second

    def __call__(self):
        print(self.first_, self.second_)
        time.sleep(10)
        return self.first_ + self.second_


models = [
    Model('example-model', lambda parameters: ExampleModel(**parameters))
        .parametrize('first', [0, 1])
        .parametrize('second', [1, 10, 100])
]

main(models, 3, ('localhost', 8000))
