from lregression import *
import math

def read_samples(filename, start=None, end=None):
    samples = dict()
    f = open(filename, "r")
    for line in f.readlines()[start:end]:
        cols = [float(x) for x in line.split()]
        samples[tuple(cols[:-1])] = cols[len(cols) - 1]
    return samples

def transform_samples(samples, phi=lambda x: x):
    t_samples = dict()
    for s in samples.keys():
        t_samples[phi(s)] = samples[s]
    return t_samples


def phi((x1, x2)):
    return (x1, x2, x1**2, x2**2, x1 * x2, math.fabs(x1 - x2), math.fabs(x1 + x2))

if __name__ == '__main__':

    in_samples = transform_samples(read_samples("in.dta"), phi)
    out_samples = transform_samples(read_samples("out.dta"), phi)
    k = range(-20, 20)
    # k = [3]
    best = (1, 0)
    for reg_lambda in k:
        lreg = Regression()
        lreg.train(in_samples, reg_l=10**reg_lambda)
        n_correct_in = 0
        n_false_in = 0
        n_correct_out = 0
        n_false_out = 0
        for x in in_samples.keys():
            res = lreg.classify([1] + list(x))
            if ((res < 0 and in_samples[x] < 0)
                    or (res > 0 and in_samples[x] > 0)):
                n_correct_in += 1
            else:
                n_false_in += 1
        for x in out_samples.keys():
            res = lreg.classify([1] + list(x))
            if ((res < 0 and out_samples[x] < 0)
                    or (res > 0 and out_samples[x] > 0)):
                n_correct_out += 1
            else:
                n_false_out += 1
        e_out = (float(n_false_out) / len(out_samples.keys()))
        if (best[0] > e_out):
            best = (e_out, reg_lambda)
        print "{0} C_in {1}".format(reg_lambda, float(n_correct_in) / len(in_samples.keys()))
        print "{0} E_in {1}".format(reg_lambda, float(n_false_in) / len(in_samples.keys()))
        print "{0} C_out {1}".format(reg_lambda, float(n_correct_out) / len(out_samples.keys()))
        print "{0} E_out {1}".format(reg_lambda, e_out)
    print best
