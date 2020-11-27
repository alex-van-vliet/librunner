from .controller import Controller
from .process import Process


def main(process: Process, models: list):
    if process.rank() == 0:
        controller = Controller(process, models)
        controller()
