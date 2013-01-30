import random
import numpy
import itertools
from  perceptron import Perceptron


class Regression(object):

    def __init__(self, weights=None):
        self.weights = weights

    def classify(self, input_vector):
        return numpy.dot(self.weights.T, input_vector)[0, 0]

    def train(self, training_set, reg_l=0):
        k = training_set.keys()
        x = numpy.matrix([[1] + list(e) for e in k])
        y = numpy.matrix([[training_set[i]] for i in k])
        pseudo_inv = (x.T * x + reg_l * numpy.identity(x.shape[1])).I * x.T
        # pseudo_inv = (x.T * x).I * x.T
        self.weights = pseudo_inv * y


def generate_random_function():
    x1, y1 = random.uniform(-1, 1), random.uniform(-1, 1)
    x2, y2 = random.uniform(-1, 1), random.uniform(-1, 1)
    a = (y2 - y1) / (x2 - x1)
    b = y1 - a * x1

    def f(x1, x2):
        if (a * x1 + b < x2):
            return 1
        else:
            return -1
    return a, b, f


# Generate samples for the function f
def generate_samples(f, num_samples):
    samples = dict()
    while len(samples) < num_samples:
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        samples[(x, y)] = f(x, y)
    return samples

if __name__ == '__main__':

    n_samples = 10
    n_out_samples = 1000
    n_runs = 1000
    n_correct_in = 0
    n_false_in = 0
    n_correct_out = 0
    n_false_out = 0
    n_iterations = 0

    for i in range(n_runs):
        a, b, f = generate_random_function()
        print "f(x)={0}*x + {1}".format(a, b)
        samples = generate_samples(f, n_samples)
        out_samples = generate_samples(f, n_out_samples)
        lregression = Regression()
        lregression.train(samples)
        w = list(itertools.chain(*lregression.weights.tolist()))
        p = Perceptron(weights=w[1:], bias=w[0])
        n_iterations += p.train(samples)
        for x, y in samples.keys():
            res = lregression.classify([[1], [x], [y]])
            if ((res < 0 and samples[(x, y)] < 0)
                    or (res > 0 and samples[(x, y)] > 0)):
                n_correct_in += 1
            else:
                n_false_in += 1
        for x, y in out_samples.keys():
            res = lregression.classify([[1], [x], [y]])
            if ((res < 0 and out_samples[(x, y)] < 0)
                    or (res > 0 and out_samples[(x, y)] > 0)):
                n_correct_out += 1
            else:
                n_false_out += 1

    print "Correct: C_in {0}".format(n_correct_in)
    print "False: E_in {0}".format(n_false_in)
    print "p_correct C_in {0}".format(float(n_correct_in) / (n_samples * n_runs))
    print "p_false E_in {0}".format(float(n_false_in) / (n_samples * n_runs))
    print "Correct: C_out {0}".format(n_correct_out)
    print "False: E_out {0}".format(n_false_out)
    print "p_correct C_out {0}".format(float(n_correct_out) / (n_out_samples * n_runs))
    print "p_false E_out {0}".format(float(n_false_out) / (n_out_samples * n_runs))
    print "Total perceptron iterations: {0}".format(float(n_iterations) / (n_runs))
