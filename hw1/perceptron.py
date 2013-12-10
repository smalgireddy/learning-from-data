import sys
sys.path.append('..')

import numpy as np
import random

from common.model import Model
from common.question import Question


class Perceptron(Model):
    def __init__(self, training_set=None, testing_set=None):
        Model.__init__(self, training_set, testing_set)
        self.weights = np.array([0., 0., 0.])
        # points that define the target function
        self.point1 = (random.uniform(-1, 1), random.uniform(-1, 1))
        self.point2 = (random.uniform(-1, 1), random.uniform(-1, 1))

    def target(self, x, y):
        x1, y1 = self.point1
        x2, y2 = self.point2
        slope = (y2 - y1) / (x2 - x1)
        # simple check to see if point (x, y) is above or below the line
        return 1 if y > (slope * (x - x1) + y1) else -1

    def hypothesis(self, x, y):
        feature = np.array([1., x, y])
        return 1 if np.dot(self.weights, feature) > 0 else -1

    def train(self):
        misclassified = []
        iterations = 0

        while True:
            # pick a point and check if it's misclassified
            for x, y in self.training_set:
                intended = self.target(x, y)

                if self.hypothesis(x, y) != intended:
                    misclassified += [((x, y), intended)]

            # set is completely separated
            if not misclassified:
                break
            # pick a random misclassified point
            # and adjust the perceptron in its direction
            else:
                iterations += 1
                point, intended = random.choice(misclassified)
                adapt = np.array([1., point[0], point[1]]) * intended
                self.weights += adapt
                misclassified = []

        return iterations

    def test(self):
        mismatches = 0

        for x, y in self.testing_set:
            if self.hypothesis(x, y) != self.target(x, y):
                mismatches += 1

        return mismatches / float(len(self.testing_set))


def test_run(data_size, test_runs):
    training_size = testing_size = data_size

    avg_iterations = 0
    avg_error = 0

    for i in xrange(test_runs):
        training_set = [(random.uniform(-1, 1), random.uniform(-1, 1))
                        for i in xrange(training_size)]
        testing_set = [(random.uniform(-1, 1), random.uniform(-1, 1))
                       for i in xrange(testing_size)]

        pla = Perceptron(training_set=training_set, testing_set=testing_set)

        avg_iterations += pla.train()
        avg_error += pla.test()

    avg_iterations /= float(test_runs)
    avg_error /= float(test_runs)
    return avg_iterations, avg_error


if __name__ == "__main__":
    question7 = Question("[n = 10] average number of iterations to converge",
                         [1, 15, 300, 5000, 10000], 'b', Question.abs_to_zero)

    question8 = Question("[n = 10] average error",
                         [0.001, 0.01, 0.1, 0.5, 0.8], 'c', Question.closest)

    question9 = Question("[n = 100] average number of iterations to converge",
                         [50, 100, 500, 1000, 5000], 'b', Question.abs_to_zero)

    question10 = Question("[n = 100] average error",
                          [0.001, 0.01, 0.1, 0.5, 0.8], 'b', Question.closest)

    # first test run with n = 10
    iterations, error = test_run(10, 1000)

    question7.check(iterations)

    # [n = 10] average number of iterations to converge
    #         result: 10.894   nearest: b. 15         answer: b. 15   CORRECT

    question8.check(error)

    # [n = 10] average error
    #         result: 0.1147   nearest: c. 0.1        answer: c. 0.1  CORRECT

    # second test run with n = 100
    iterations, error = test_run(100, 1000)

    question9.check(iterations)

    # [n = 100] average number of iterations to converge
    #         result: 119.366  nearest: b. 100        answer: b. 100  CORRECT

    question10.check(error)

    # [n = 100] average error
    #         result: 0.01299  nearest: b. 0.01       answer: b. 0.01 CORRECT
