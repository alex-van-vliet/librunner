from .process import Process


def main(process: Process, models: list):
    if process.rank() == 0:
        for i, model in enumerate(models):
            print(f'Model {i}: {model.name()}')
            for parameters in model():
                print(parameters)
