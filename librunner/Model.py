class Model:
    name_: str
    creator_: callable
    parameters_: list

    def __init__(self, name, creator):
        self.name_ = name
        self.creator_ = creator
        self.parameters_ = []

    def name(self):
        return self.name_

    def parametrize(self, name: str, values: list) -> 'Model':
        self.parameters_.append((name, values))
        return self

    def __call__(self):
        current_parameters = [0] * len(self.parameters_)

        def generate(i):
            if i == len(self.parameters_):
                yield current_parameters
            else:
                for selected in range(len(self.parameters_[i][1])):
                    current_parameters[i] = selected
                    yield from generate(i + 1)

        yield from generate(0)
