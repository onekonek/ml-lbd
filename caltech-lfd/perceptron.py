import random


def inner_product(vector_a, vector_b):
    total = 0
    for a, b in zip(vector_a, vector_b):
        total += (a * b)
    return total


class Perceptron(object):

    def __init__(self, weights=None, bias=0.5):
        self.bias = bias
        self.weights = weights

    def classify(self, input_vector):
        if inner_product(self.weights, input_vector) < self.bias:
            return -1
        else:
            return 1

    def train(self, training_set, alpha=1, max_iterations=None):
        if self.weights is None:
            print "Initializing weights to 0"
            self.weights = [0] * len(training_set.keys()[0])
        n = 0
        updated = True
        while(updated):
            updated = False
            samples = training_set.items()
            random.shuffle(samples)
            for x, y in samples:
                y_p = self.classify(x)
                if(y != y_p):
                    self.update_weights(alpha, y, y_p, x)
                    self.update_bias(alpha, y, y_p)
                    updated = True
                    n += 1
                    if max_iterations is not None and n >= max_iterations:
                        break
        return n

    def apply(self, test_set):
        for x, y in test_set.items():
            if(self.classify(x) != y):
                return False
        return True

    def update_weights(self, alpha, t, y, x):
        for i in range(len(self.weights)):
            self.weights[i] = (alpha * (t - y) * x[i]) + self.weights[i]

    def update_bias(self, alpha, t, y):
        self.bias = (alpha * (t - y) * -1) + self.bias


# Generate samples for the function f(x)=y
def generate_samples(num_samples):
    samples = dict()
    while len(samples) < num_samples:
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        if (x < y):
            samples[(x, y)] = 1
        elif (x > y):
            samples[(x, y)] = -1
    return samples


if __name__ == '__main__':

    # How many runs
    num_runs = 1000
    # How many samples to train on
    num_samples = 10
    # How many samples to use for testing
    num_test_samples = 10000
    total_iterations = 0
    total_p = 0

    for i in range(num_runs):
        print "Run {0} of {1}".format(i, num_runs)
        nn = Perceptron()
        samples = generate_samples(num_samples)
        total_iterations += nn.train(samples, alpha=1, max_iterations=None)
        test_samples = generate_samples(num_test_samples)
        n_correct = 0
        n_false = 0
        for x, y in test_samples.items():
            y_p = nn.classify(x)
            if (y_p == y):
                n_correct += 1
            else:
                n_false += 1
        total_p += (float(n_false) / (n_false + n_correct))

    print "Average iterations: {0}".format(total_iterations / num_runs)
    print "P(f(x) != g(x)): {0}".format(total_p / num_runs)
