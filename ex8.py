import lregression
import numpy
import random


def f(x_1, x_2):
    if ((x_1 * x_1 + x_2 * x_2 - 0.6) < 0):
        return -1
    else:
        return 1


def transform(s):
    x, y = s
    return (x, y, x*y, x*x, y*y)


def transform_samples(f, samples):
    new_samples = dict()
    for sample in samples.keys():
        new_samples[f(sample)] = samples[sample]
    return new_samples


def add_noise(samples, fraction):
    subset = dict()
    while (len(subset.keys()) < flip_fraction * len(samples)):
        sample = random.choice(samples.keys())
        samples[sample] = samples[sample] * -1
        subset[sample] = 1


if __name__ == '__main__':
    n_samples = 1000
    flip_fraction = 0.1
    n_out_samples = 1000
    n_runs = 1000
    n_correct_in = 0
    n_false_in = 0
    n_correct_out = 0
    n_false_out = 0
    total_weight = None

    for i in range(n_runs):
        samples = lregression.generate_samples(f, n_samples)
        trans_samples = transform_samples(transform, samples)
        out_samples = lregression.generate_samples(f, n_out_samples)
        trans_samples = transform_samples(transform, samples)
        out_trans_samples = transform_samples(transform, out_samples)
        add_noise(trans_samples, flip_fraction)
        add_noise(out_trans_samples, flip_fraction)
        lreg = lregression.Regression()
        lreg.train(trans_samples)
        if total_weight == None:
            total_weight = lreg.weights
        else:
            total_weight += lreg.weights
        for sample in trans_samples.keys():
            test = [[1]] + [[x] for x in list(sample)]
            res = lreg.classify(test)
            if ((res < 0 and trans_samples[sample] < 0)
                    or (res > 0 and trans_samples[sample] > 0)):
                n_correct_in += 1
            else:
                n_false_in += 1
        for sample in out_trans_samples.keys():
            test = [[1]] + [[x] for x in list(sample)]
            res = lreg.classify(test)
            if ((res < 0 and out_trans_samples[sample] < 0)
                    or (res > 0 and out_trans_samples[sample] > 0)):
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
    print "{0}".format(total_weight / float(n_runs))
    print "{0}".format(total_weight)
