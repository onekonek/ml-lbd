import itertools
import random

def sign_permutations(length):
    """ Memory efficient generator: generate all n^2 sign permutations. """ 
    # return a generator which generates the product of "length" smaller 
    # generators of (-1 or +1) (i.e. the unrolled signs, evaulated as needed)
    return itertools.product([-1, 1], repeat=length)

def random_product(*args, **kwds):
    """ Random selection from itertools.product(*args, **kwds). """
    pools = map(tuple, args) * kwds.get('repeat', 1)
    limiter = 0
    generate_limit = kwds.get('generate_limit', None)
    while True if generate_limit == None else limiter < generate_limit:
      limiter = limiter + 1
      yield tuple(random.choice(pool) for pool in pools)

def random_sign_permutations(length, limit):
    """ Random sign permutation generator. """
    return random_product([-1, 1], repeat=length, generate_limit=limit)

def binary_combinations(length, sublength, comb_function = itertools.combinations, limit=None):
    """ Memory efficient generator: generate all length choose sublength combinations. """ 

    # get the combination indices, support both infinite and finite length generators
    combination_indices = comb_function(range(length), sublength, limit) if limit else comb_function(range(length), sublength)

    def indices_to_sign_vectors():
      """ Generates sign vectors from indices. """
      for index_tuple in combination_indices:
        for i in xrange(length):
          yield 1 if index_tuple.count(i) > 0 else 0

    def grouper(n, iterable, fillvalue=None):
      " For grouping a generated stream into tuples. "
      args = [iter(iterable)] * n
      return itertools.izip_longest(fillvalue=fillvalue, *args)

    # generate all combinations, grouped into tuples
    return grouper(length, indices_to_sign_vectors())

def random_combination(iterable, r, generate_limit=None):
    """ Random selection from itertools.combinations(iterable, r). """
    pool = tuple(iterable)
    n = len(pool)
    limiter = 0
    while True if generate_limit == None else limiter < generate_limit:
      limiter = limiter + 1
      indices = sorted(random.sample(xrange(n), r))
      yield tuple(pool[i] for i in indices)

def random_binary_combinations(length, sublength, limit):
    """ Random combination generator. """
    return binary_combinations(length, sublength, random_combination, limit)

