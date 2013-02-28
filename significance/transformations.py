import numpy
from scipy import stats

def identity (data):
    """ Returns identity-transformation of the input data """
    return data
    
def signed_rank (data):
    """ Returns the signed ranks of the input data """
    signs = numpy.vectorize(lambda num: 1 if num >= 0 else -1)
    data_signs = signs(data)
    # rank assignment, with midranks in case of ties
    data_ranks = numpy.round(stats.rankdata(numpy.abs(data))).astype(int)
    return data_signs*data_ranks
    
def rank_order (data):
    """ Returns the simple ranks of the input data """
    # rank assignment, with midranks in case of ties
    data_ranks = numpy.round(stats.rankdata(data)).astype(int)
    return data_ranks
