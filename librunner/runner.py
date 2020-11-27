from .process import Process


class Runner:
    process_: Process
    models_: list

    def __init__(self, process, models):
        self.process_ = process
        self.models_ = models

    def __call__(self):
        print('Hi from runner')
