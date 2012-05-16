import random
import math
import numpy
import perceptron
import itertools


class LogRegression(object):

    def __init__(self, weights=None):
        self.weights = weights

    def classify(self, input_vector):
        s = perceptron.inner_product(self.weights, (1,) + input_vector)
        return math.exp(s) / (1 + math.exp(s))

    def train_sgd(self, training_set, epsilon, learning_rate):
        samples = training_set.keys()
        if (self.weights == None):
            self.weights = [0] + [0 for item in samples[0]]
        converged = False
        num_epochs = 0
        while (not converged):
            old_weight = self.weights
            numpy.random.shuffle(samples)
            for sample in samples:
                grad = self.gradient(sample, training_set[sample])
                self.weights = [w - learning_rate * g for w, g in zip(self.weights, grad)]
            num_epochs += 1
            converged = self.vector_norm([a - b for a, b in zip(old_weight, self.weights)]) < epsilon
        return num_epochs

    def gradient(self, sample, y):
        vec = [y * 1] + [float(y) * x for x in sample]
        div = (1.0 + math.exp(float(y) * perceptron.inner_product((1,) + sample, self.weights)))
        vec = [-1.0 * x / div for x in vec]
        return vec

    def vector_norm(self, vector):
        return math.sqrt(sum([x ** 2 for x in vector]))

    def cross_entropy_error(self, sample, y):
        return math.log(1.0 + math.exp(-y * perceptron.inner_product((1,) + sample, self.weights)))

    def total_ce_error(self, samples):
        error = 0
        for sample in samples.keys():
            error += self.cross_entropy_error(sample, samples[sample])
        return 1.0 / len(samples) * error


def generate_random_function():
    x1, y1 = random.uniform(-1, 1), random.uniform(-1, 1)
    x2, y2 = random.uniform(-1, 1), random.uniform(-1, 1)
    a = (y2 - y1) / (x2 - x1)
    b = y1 - a * x1

    def f(x1, x2):
        if (a * x1 + b < x2):
            return 1.0
        else:
            return -1.0
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

    n_samples = 100
    n_out_samples = 100000
    n_runs = 100
    n_epochs = 0
    n_e_out = 0
    sgd_learning_rate = 0.1
    sgd_epsilon = 0.005

    for i in range(n_runs):
        a, b, f = generate_random_function()
        print "{0}: f(x)={1}*x + {2}".format(i, a, b)
        samples = generate_samples(f, n_samples)
        out_samples = generate_samples(f, n_out_samples)
        log_reg = LogRegression()
        epochs = log_reg.train_sgd(samples, sgd_epsilon, sgd_learning_rate)
        e_out = log_reg.total_ce_error(out_samples)
        print "{0}: epochs: {1}".format(i, epochs)
        print "{0}: e_out: {1}".format(i, e_out)
        n_e_out += e_out
        n_epochs += epochs
    print "Average # of epochs: {0}".format(n_epochs / float(n_runs))
    print "Average e_out: {0}".format(n_e_out / float(n_runs))
