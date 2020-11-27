from librunner.Model import Model
from librunner.process import Process
from librunner.main import main

process = Process()


class ExampleModel:
    def __init__(self, **kwargs):
        print(kwargs)


models = [
    Model('example-model', lambda parameters: ExampleModel(**parameters))
        .parametrize('first', [0, 1])
        .parametrize('second', [1, 10, 100])
]

main(process, models)
