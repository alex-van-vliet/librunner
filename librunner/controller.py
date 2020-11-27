from typing import Generator, Optional, Tuple, Any, List

from .model import Model
from .process import Process


class Controller:
    process_: Process
    models_: List[Model]
    generator_: Optional[Generator[Tuple[int, Any], None, None]]
    ended_: bool
    left_: int

    def __init__(self, process, models):
        self.process_ = process
        self.models_ = models
        self.generator_ = None
        self.left_ = 0

    def send_all(self):
        for i in range(1, self.process_.size()):
            try:
                data = next(self.generator_)
                self.left_ += 1
                self.process_.send(i, data)
            except StopIteration:
                self.generator_ = None
                break

    def quit(self):
        for i in range(1, self.process_.size()):
            self.process_.send(i, None)

    def __call__(self):
        def models():
            for i, model in enumerate(self.models_):
                for parameters in model():
                    yield i, parameters

        self.left_ = 0
        self.generator_ = models()
        self.send_all()
        results = []
        while self.left_ > 0:
            source, result = self.process_.recv_any()
            results.append(result)
            self.left_ -= 1
            if self.generator_:
                try:
                    data = next(self.generator_)
                    self.left_ += 1
                    self.process_.send(source, data)
                except StopIteration:
                    self.generator_ = None
        print('Finished, quitting runners...')
        self.quit()
        print('Top 3 runs:')
        results = sorted(results, key=lambda v: v[-1], reverse=True)
        for model, parameters, score in results[:3]:
            print(f'Score: {score}, parameters: '
                  + ', '.join(f'{key}={repr(value)}'
                              for key, value
                              in self.models_[model].values(parameters).items()))
