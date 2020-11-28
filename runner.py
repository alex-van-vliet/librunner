from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier

from librunner.main import main, print_results
from librunner.model import Model


class KNeighbors:
    n_neighbors_: int

    def __init__(self, n_neighbors):
        self.n_neighbors_ = n_neighbors

    def __call__(self, data):
        X, y = data
        X_train, X_val, y_train, y_val = train_test_split(X, y)

        classifier = KNeighborsClassifier(n_neighbors=self.n_neighbors_)
        classifier.fit(X_train, y_train)

        return classifier.score(X_val, y_val)


class RandomForest:
    n_estimators_: int
    max_depth_: int

    def __init__(self, n_estimators, max_depth):
        self.n_estimators_ = n_estimators
        self.max_depth_ = max_depth

    def __call__(self, data):
        X, y = data
        X_train, X_val, y_train, y_val = train_test_split(X, y)

        classifier = RandomForestClassifier(n_estimators=self.n_estimators_, max_depth=self.max_depth_)
        classifier.fit(X_train, y_train)

        return classifier.score(X_val, y_val)


models = [
    Model('KNeighbors', lambda parameters: KNeighbors(**parameters))
        .parametrize('n_neighbors', [1, 5, 10, 20, 40]),
    Model('RandomForest', lambda parameters: RandomForest(**parameters))
        .parametrize('n_estimators', [50, 100, 200])
        .parametrize('max_depth', [5, 10, 15])
]

results = main(load_digits(return_X_y=True), models, 3, ('localhost', 8000))
print_results(models, results, k=None)
