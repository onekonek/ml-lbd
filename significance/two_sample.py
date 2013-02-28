import numpy
import generators

# Generalized two-sample permutation test

def perm_test (data1, data2, transformation):
    """ Conducts a permutation test on the input data, transformed by fun. """
    # apply transformation to input data (e.g. signed-rank for WMW)
    data = transformation(numpy.concatenate((data1, data2)))
    data1 = data[0:len(data1)]
    stat_ref = numpy.sum(data1)
    # count permutation test statistics <=, >=, or ||>=|| than reference stat   
    counts = numpy.array([0,0,0]) # (lesser, greater)

    for binary_row in generators.binary_combinations(len(data),len(data1)):
        stat_this = numpy.sum(numpy.array(data)*binary_row)
        counts = counts + stat_compare(stat_ref,stat_this)
    # return p-values for lower, upper, and two-tail tests (FP number)
    n_comb = numpy.multiply.reduce(numpy.array(range(len(data)-len(data1)+1,len(data)+1)))\
           / numpy.multiply.reduce(numpy.array(range(1,len(data1)+1)))
    counts[2] = min(2*counts[0:2].min(),n_comb) # hack to define p.twotail as 2*smaller of 1 tail p's

    return counts / float(n_comb)

def stat_compare (stat_ref,stat_test):
    """ Tests for comparing permutation and observed test statistics"""
    lesser = (1 if stat_test <= stat_ref else 0)
    greater = (1 if stat_test >= stat_ref else 0)
    more_extreme = 0
    return numpy.array([lesser,greater,more_extreme])
