from typing import List

from .controller import Controller
from .model import Model
from .process import Process
from .runner import Runner


def main(process: Process, models: List[Model]):
    if process.rank() == 0:
        controller = Controller(process, models)
        controller()
    else:
        runner = Runner(process, models)
        runner()
