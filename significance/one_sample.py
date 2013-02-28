import numpy
import generators

# Generalized one-sample permutation test

def perm_test (data, transformation):
    """ Conducts a permutation test on the input data, transformed by fun. """
    # apply transformation to input data (e.g. signed-rank for Wilcoxon)
    data = transformation(data)
    stat_ref = numpy.sum(data)
    # count permutation test statistics <=, >=, or ||>=|| than reference stat   
    counts = numpy.array([0,0,0]) # (lesser, greater, more extreme)
    for sign_row in generators.sign_permutations(len(data)):
        stat_this = numpy.sum(numpy.array(data)*sign_row)
        counts = counts + stat_compare(stat_ref,stat_this)
    # return p-values for lower, upper, and two-tail tests (FP number)
    return counts / 2.0**len(data)


def stat_compare (stat_ref,stat_test):
    """ Tests for comparing permutation and observed test statistics"""
    lesser = (1 if stat_test <= stat_ref else 0)
    greater = (1 if stat_test >= stat_ref else 0)
    more_extreme = (1 if numpy.abs(stat_test) >= numpy.abs(stat_ref) else 0)
    return numpy.array([lesser,greater,more_extreme])
