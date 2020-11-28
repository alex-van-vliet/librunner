from typing import List

from .controller import Controller
from .model import Model


def main(models: List[Model], nb_children: int):
    controller = Controller(models, nb_children)
    controller()
