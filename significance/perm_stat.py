import transformations
import one_sample
import two_sample

# Specific permutation tests

def fisher_perm_test (data):
    """ Conducts a fisher permutation test"""
    return one_sample.perm_test (data, transformations.identity)
    
def wilcoxon_perm_test (data):
    """ Conducts a wilcoxon signed-rank test"""
    return one_sample.perm_test (data, transformations.signed_rank)
    
def pitman_perm_test (data1, data2):
    """ Conducts a pitman permutation test"""
    return two_sample.perm_test (data1, data2, transformations.identity)

def wmw_perm_test (data1, data2):
    """ Conducts a wilcoxon-mann-whitney permutation test"""
    return two_sample.perm_test (data1, data2, transformations.rank_order)
