from typing import List

from .controller import Controller
from .model import Model


def main(models: List[Model], nb_children: int):
    with Controller(models, nb_children) as controller:
        controller()
