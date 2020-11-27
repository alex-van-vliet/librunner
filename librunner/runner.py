from .process import Process


class Runner:
    process_: Process
    models_: list

    def __init__(self, process, models):
        self.process_ = process
        self.models_ = models

    def __call__(self):
        while True:
            model, parameters = self.process_.recv(0)
            result = self.models_[model].create(parameters)()
            self.process_.send(0, (model, parameters, result))
