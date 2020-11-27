from typing import Generator, Optional, Tuple, Any

from .process import Process


class Controller:
    process_: Process
    models_: list
    sent_: dict
    generator_: Optional[Generator[Tuple[int, Any], None, None]]
    ended_: bool

    def __init__(self, process, models):
        self.process_ = process
        self.models_ = models
        self.sent_ = {}
        self.generator_ = None

    def send_all(self):
        for i in range(1, self.process_.size_):
            try:
                data = next(self.generator_)
                self.process_.send(i, data)
            except StopIteration:
                self.generator_ = None
                break

    def __call__(self):
        def models():
            for i, model in enumerate(self.models_):
                for parameters in model():
                    yield i, parameters

        self.generator_ = models()
        self.send_all()
        while True:
            source, (model, parameters, score) = self.process_.recv_any()
            print(source, model, parameters, score)
