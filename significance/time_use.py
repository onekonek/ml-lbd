#!/usr/bin/env python
# Example uses of permtst

from perm_stat import *
import numpy
import random
from timeit import Timer

REPEATED_TRIALS = 10
REPEATED_TESTS = 3
FAILING_CONDITION = 200   # fail if prev test takes longer than this number of seconds

print "- - - - - - - Two Sample Tests - - - - - - -"
print " "

for datalen in xrange(1, 25): 

  # collect results
  t = Timer(stmt="pitman_perm_test(x,y)", 
            setup="from time_use import datalen; import random; \
                   import numpy; from perm_stat import pitman_perm_test; \
                   x = numpy.array([random.uniform(0,10) for zz in xrange(0,datalen)]); \
                   y = numpy.array([random.uniform(0,10) for zz in xrange(0,datalen)]);")
  # conduct fine grained repeated trials and coarse grained repeated trials, as recommended
  prev_time = min(t.repeat(repeat=REPEATED_TESTS, number=REPEATED_TRIALS))  

  # print out results
  print str(datalen) + ", ", str(prev_time) + " s"

  # enforce failing condition
  if prev_time > FAILING_CONDITION:
    break

