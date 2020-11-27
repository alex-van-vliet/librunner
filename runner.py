from librunner.Model import Model
from librunner.process import Process
from librunner.main import main

process = Process()


class ExampleModel:
    first_: int
    second_: int

    def __init__(self, first, second):
        self.first_ = first
        self.second_ = second

    def __call__(self):
        print(self.first_, self.second_)
        return self.first_ + self.second_


models = [
    Model('example-model', lambda parameters: ExampleModel(**parameters))
        .parametrize('first', [0, 1])
        .parametrize('second', [1, 10, 100])
]

main(process, models)
