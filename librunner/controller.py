from .process import Process


class Controller:
    process_: Process
    models_: list

    def __init__(self, process, models):
        self.process_ = process
        self.models_ = models

    def __call__(self):
        for i, model in enumerate(self.models_):
            print(f'Model {i}: {model.name()}')
            for parameters in model():
                print(parameters)
