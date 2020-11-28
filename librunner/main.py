from typing import List, Tuple, Optional

from .controller import Controller
from .model import Model


def main(models: List[Model], nb_children: int, address: Tuple[str, int]):
    with Controller(models, nb_children, address) as controller:
        controller()
        return controller.results()


def print_results(models: List[Model], results: List[Tuple[int, List[int], float]], k: Optional[int] = 3):
    if k is None:
        k = len(results)
        print('All runs:')
    else:
        print(f'Top {k} runs:')
    for model, parameters, score in results[:k]:
        print(f'Score: {score}, parameters: '
              + ', '.join(f'{key}={repr(value)}'
                          for key, value
                          in models[model].values(parameters).items()))
