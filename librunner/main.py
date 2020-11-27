from .controller import Controller
from .process import Process
from .runner import Runner


def main(process: Process, models: list):
    if process.rank() == 0:
        controller = Controller(process, models)
        controller()
    else:
        runner = Runner(process, models)
        runner()
