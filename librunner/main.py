from typing import List, Tuple

from .controller import Controller
from .model import Model


def main(models: List[Model], nb_children: int, address: Tuple[str, int]):
    with Controller(models, nb_children, address) as controller:
        controller()
