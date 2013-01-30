from perceptron import Perceptron, inner_product
from lregression import generate_random_function
from cvxopt import matrix, solvers
import cvxopt
import random
import numpy as np


class SVM(object):

    def __init__(self, weights=None):
        self.weights = weights

    def train(self, samples):
        X_l = []
        y_l = []
        for x, y_s in samples.items():
          X_l.append(list(x[1:]))
          y_l.append(float(y_s))
        X = np.array(X_l)
        y = np.array(y_l)
        # Gram matrix
        n_samples, n_features = X.shape
        K = np.zeros((n_samples, n_samples))
        for i in range(n_samples):
            for j in range(n_samples):
                K[i, j] = np.dot(X[i], X[j])
        P = cvxopt.matrix(np.outer(y, y) * K)
        q = cvxopt.matrix(np.ones(n_samples) * -1)
        A = cvxopt.matrix(y, (1, n_samples))
        b = cvxopt.matrix(0.0)
        G = cvxopt.matrix(np.diag(np.ones(n_samples) * -1))
        h = cvxopt.matrix(np.zeros(n_samples))
        # solve QP problem
        solution = cvxopt.solvers.qp(P, q, G, h, A, b)
        # solution = cvxopt.solvers.qp(P, q, G=G, h=h, A=A, b=b)
        a = np.ravel(solution['x'])
        ssv = a > 1e-5
        ind = np.arange(len(a))
        ind = ind[ssv]
        a = a[ssv]
        sv = X[ssv]
        sv_y = y[ssv]
        # print("{0} support vectors out of {1} points".format(len(a), n_samples))
        # print "sv", sv
        # print "sv_y", sv_y
        self.b = 0
        for n in range(len(a)):
          self.b += sv_y[n]
          self.b -= np.sum(a * sv_y * K[ind[n], ssv])
        self.b /= len(a)

        self.w = np.zeros(n_features)
        for n in range(len(a)):
          self.w += a[n] * sv_y[n] * sv[n]
        return len(a)

    def classify(self, sample):
        s = list(sample[1:])
        r = np.dot(s, self.w) + self.b
        if (r < 0):
          return -1
        else:
          return 1


def generate_samples(f, num_samples):
    samples = dict()
    while len(samples) < num_samples:
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        samples[(1, x, y)] = f(x, y)
    t = set()
    for x, y in samples.items():
      t.add(y)
    if (len(t) != 2):
      return generate_samples(f, num_samples)
    return samples

def eval(samples, classifier):
  n_correct = 0
  n_false = 0
  n_total = 0
  for x, y in samples.items():
      res = classifier.classify(list(x))
      if ((res < 0 and y < 0)
              or (res > 0 and y > 0)):
          n_correct += 1
          n_total += 1
      else:
          n_false += 1
          n_total += 1
  return n_correct, n_false, n_total

if __name__ == '__main__':

    # How many runs
    num_runs = 1000
    # How many samples to train on
    n_samples = 10
    # How many samples to use for testing
    n_out_samples = 10000

    n_svm_better = 0
    n_svm_svs_total = 0

    for i in range(num_runs):
        print "Run {0} of {1}".format(i, num_runs)
        a, b, f = generate_random_function()
        print "f(x)={0}*x + {1}".format(a, b)
        samples = generate_samples(f, n_samples)
        out_samples = generate_samples(f, n_out_samples)
        nn = Perceptron()
        svm = SVM()
        nn.train(samples, alpha=1, max_iterations=None)
        n_sv = svm.train(samples)
        n_svm_svs_total += n_sv
        n_p_correct, n_p_false, n_p_total = eval(out_samples, nn)
        n_svm_correct, n_svm_false, n_svm_total = eval(out_samples, svm)
        print "Perceptron: P(f(x) != g(x)): {0}".format(float(n_p_false) / n_p_total)
        print "SVM: P(f(x) != g(x)): {0}".format(float(n_svm_false) / n_svm_total)
        if (n_svm_correct > n_p_correct):
          n_svm_better += 1
    print "SVM was better in {0} cases: {1}%".format(n_svm_better, 100 * n_svm_better / float(num_runs))
    print "Average #SVs: {0}".format(n_svm_svs_total / float(num_runs))
